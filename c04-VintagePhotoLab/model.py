# ============================================================================
# DeOldify WebApp — Model definitions & image processing pipeline
# ----------------------------------------------------------------------------
# Author : Tariq Jamil
# Version: 1.0.0
# Date   : 2025-06-14
# License: MIT
# ============================================================================

import os
import warnings
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn as nn
import requests
from PIL import Image, ImageEnhance, ImageOps, ImageFilter as PILFilter

torch.set_num_threads(1)
warnings.filterwarnings("ignore", ".*torch.distributed.*")

_HF_DATA = Path("/data")
MODEL_DIR = _HF_DATA / "models" if _HF_DATA.is_dir() else Path(__file__).parent / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Remote model weight URLs (auto-downloaded on first use)
# ---------------------------------------------------------------------------
MODEL_URLS = {
    "ColorizeArtistic_gen.pth": ("https://huggingface.co/databuzzword/deoldify-artistic/resolve/main/ColorizeArtistic_gen.pth", 243 * 1024 * 1024),
    "RealESRGAN_x4plus.pth": ("https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth", 64 * 1024 * 1024),
    "GFPGANv1.4.pth": ("https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth", 333 * 1024 * 1024),
}


# ---------------------------------------------------------------------------
# Weight download helper
# ---------------------------------------------------------------------------
def _ensure_model(name: str):
    path = MODEL_DIR / name
    if path.exists() and path.stat().st_size > 1024:
        return str(path)
    url, expected = MODEL_URLS.get(name)
    if url is None:
        raise FileNotFoundError(f"No download URL for {name}")
    print(f"Downloading {name} ({expected // 1024 // 1024} MB)...")
    r = requests.get(url, stream=True, timeout=300)
    r.raise_for_status()
    tmp = path.with_suffix(".tmp")
    with open(tmp, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    tmp.rename(path)
    print(f"  done")
    return str(path)


# ============================================================================
# Colorization Model — UNet with ResNet34 encoder
# ============================================================================

class ColorizationModel(nn.Module):
    """UNet with ResNet34 encoder for image colorization (RGB output)."""

    def __init__(self):
        super().__init__()
        from torchvision import models as tv_models
        resnet = tv_models.resnet34(weights=tv_models.ResNet34_Weights.IMAGENET1K_V1)

        self.enc_conv1 = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu)  # 64
        self.enc_maxpool = resnet.maxpool
        self.enc_layer1 = resnet.layer1  # 64
        self.enc_layer2 = resnet.layer2  # 128
        self.enc_layer3 = resnet.layer3  # 256
        self.enc_layer4 = resnet.layer4  # 512

        # Up-path: upsample → cat → conv
        def _up(in_ch, out_ch):
            return nn.Sequential(
                nn.Conv2d(in_ch, out_ch, 3, padding=1),
                nn.BatchNorm2d(out_ch), nn.ReLU(True),
            )

        self.up4_t = nn.ConvTranspose2d(512, 256, 4, 2, 1)
        self.up4_c = _up(512, 256)
        self.up3_t = nn.ConvTranspose2d(256, 128, 4, 2, 1)
        self.up3_c = _up(256, 128)
        self.up2_t = nn.ConvTranspose2d(128, 64, 4, 2, 1)
        self.up2_c = _up(128, 64)
        self.up1_t = nn.ConvTranspose2d(64, 32, 4, 2, 1)
        self.up1_c = _up(96, 32)

        self.out = nn.Sequential(
            nn.Conv2d(32, 16, 3, padding=1), nn.ReLU(True),
            nn.Conv2d(16, 3, 1), nn.Sigmoid(),
        )

    def forward(self, x):
        f0 = self.enc_conv1(x)              # 64,  56×56
        p = self.enc_maxpool(f0)             # 64,  28×28
        f1 = self.enc_layer1(p)              # 64,  28×28
        f2 = self.enc_layer2(f1)             # 128, 14×14
        f3 = self.enc_layer3(f2)             # 256,  7×7
        f4 = self.enc_layer4(f3)             # 512,  7×7

        d = self.up4_t(f4)                   # 256, 14×14
        d = self.up4_c(torch.cat([d, f3], 1)) # 256, 14×14
        d = self.up3_t(d)                    # 128, 28×28
        d = self.up3_c(torch.cat([d, f2], 1)) # 128, 28×28
        d = self.up2_t(d)                    # 64,  56×56
        d = self.up2_c(torch.cat([d, f1], 1)) # 64,  56×56
        d = self.up1_t(d)                    # 32, 112×112
        d = self.up1_c(torch.cat([d, f0], 1)) # 32, 112×112
        return self.out(d)                    # 3,  112×112

    def load_encoder_from_deoldify(self, weights_path):
        """Load encoder weights from DeOldify state dict (best-effort)."""
        sd = torch.load(weights_path, map_location='cpu', weights_only=False)
        sd = sd['model'] if 'model' in sd else sd
        mapping = {
            'enc_conv1.0.': 'layers.0.0.',       # conv1
            'enc_conv1.1.': 'layers.0.1.',       # bn1
            'enc_layer1.':  'layers.0.4.',        # layer1
            'enc_layer2.':  'layers.0.5.',        # layer2
            'enc_layer3.':  'layers.0.6.',        # layer3
            'enc_layer4.':  'layers.0.7.',        # layer4
        }
        n = 0
        for own_key in self.state_dict():
            for prefix, deoldify_prefix in mapping.items():
                if own_key.startswith(prefix):
                    dk = own_key.replace(prefix, deoldify_prefix)
                    if dk in sd:
                        self.state_dict()[own_key].copy_(sd[dk])
                        n += 1
                    break
        print(f"Loaded {n}/{len(list(self.state_dict().keys()))} encoder keys from DeOldify")
        return n


# ============================================================================
# Colorizer — High-level wrapper for colorization inference
# ============================================================================

class Colorizer:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.ready = False

    def init(self):
        if self.ready:
            return
        self.model = ColorizationModel()
        wpath = _ensure_model("ColorizeArtistic_gen.pth")
        self.model.load_encoder_from_deoldify(wpath)
        self.model.to(self.device).eval()
        self.ready = True
        print(f"Colorizer ready on {self.device}")

    def colorize(self, img_rgb: np.ndarray) -> Image.Image:
        self.init()
        img = Image.fromarray(img_rgb).convert("RGB")
        w, h = img.size
        scale = min(224 / w, 224 / h)
        nw, nh = int(w * scale), int(h * scale)
        img_small = img.resize((nw, nh), Image.LANCZOS)
        pad_w, pad_h = 224 - nw, 224 - nh
        img_pad = Image.new("RGB", (224, 224), (0, 0, 0))
        img_pad.paste(img_small, (pad_w // 2, pad_h // 2))

        t = torch.from_numpy(np.array(img_pad).transpose(2, 0, 1)).float().div(255.).unsqueeze(0).to(self.device)
        if self.device.type == "cpu":
            t = t.half()
            with torch.no_grad():
                m = self.model.half()
                out = m(t).clamp(0, 1).squeeze(0).cpu().float().numpy().transpose(1, 2, 0)
            self.model.float()
        else:
            with torch.no_grad():
                out = self.model(t).clamp(0, 1).squeeze(0).cpu().numpy().transpose(1, 2, 0)
        out = out[pad_h // 2:pad_h // 2 + nh, pad_w // 2:pad_w // 2 + nw]
        return Image.fromarray((out * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)


# ============================================================================
# Super-Resolution — Real-ESRGAN 4x upscaling
# ============================================================================

class SuperResolution:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.upsampler = None
        self.ready = False

    def init(self):
        if self.ready:
            return
        from basicsr.archs.rrdbnet_arch import RRDBNet
        from realesrgan import RealESRGANer
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        path = _ensure_model("RealESRGAN_x4plus.pth")
        self.upsampler = RealESRGANer(
            scale=4, model_path=path, model=model,
            tile=0, tile_pad=10, pre_pad=0, device=self.device,
            fp16=self.device.type == "cpu",
        )
        self.ready = True
        print(f"SuperResolution ready on {self.device}")

    @torch.no_grad()
    def upscale(self, img_rgb: np.ndarray, scale: int = 4) -> np.ndarray:
        self.init()
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        out, _ = self.upsampler.enhance(img_bgr, outscale=scale)
        return cv2.cvtColor(out, cv2.COLOR_BGR2RGB)


# ============================================================================
# Face Restoration — GFPGAN face enhancement
# ============================================================================

class FaceRestoration:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.restorer = None
        self.ready = False

    def init(self):
        if self.ready:
            return
        from gfpgan import GFPGANer
        path = _ensure_model("GFPGANv1.4.pth")
        self.restorer = GFPGANer(
            model_path=path, upscale=1, arch='clean',
            channel_multiplier=2, device=self.device,
            fp16=self.device.type == "cpu",
        )
        self.ready = True
        print(f"FaceRestoration ready on {self.device}")

    @torch.no_grad()
    def restore(self, img_rgb: np.ndarray, weight: float = 0.5) -> np.ndarray:
        self.init()
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        _, _, restored_img = self.restorer.enhance(img_bgr, has_aligned=False, paste_back=True, weight=weight)
        if restored_img is None:
            return img_rgb
        return cv2.cvtColor(restored_img, cv2.COLOR_BGR2RGB)


# ============================================================================
# Photo Filters — 20+ artistic & classic image effects
# ============================================================================

class PhotoFilters:
    @staticmethod
    def mono(im): return ImageOps.grayscale(im).convert("RGB")

    @staticmethod
    def sepia(im):
        a = np.array(im.convert("RGB"), np.float32)
        k = np.array([[.393,.769,.189],[.349,.686,.168],[.272,.534,.131]])
        return Image.fromarray(np.clip(a @ k.T, 0, 255).astype(np.uint8))

    @staticmethod
    def film(im):
        a = np.array(im.convert("RGB"), np.float32)
        a = np.clip(a * [1., .93, .85] + np.random.randn(*a.shape).astype(np.float32) * 8, 0, 255)
        h, w = a.shape[:2]
        X, Y = np.meshgrid(np.linspace(-1, 1, w), np.linspace(-1, 1, h))
        v = np.clip(1 - np.sqrt(X**2 + Y**2) * .4, .25, 1.)
        r = ImageEnhance.Contrast(Image.fromarray((a * v[..., None]).astype(np.uint8))).enhance(1.15)
        return ImageEnhance.Brightness(r).enhance(.95)

    @staticmethod
    def canny(im, t1=50, t2=150):
        e = cv2.Canny(cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2GRAY), t1, t2)
        return Image.fromarray(cv2.cvtColor(e, cv2.COLOR_GRAY2RGB))

    @staticmethod
    def pencil(im):
        g = cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2GRAY)
        s = cv2.divide(g, 255 - cv2.GaussianBlur(255 - g, (21, 21), 0), scale=256)
        return Image.fromarray(cv2.cvtColor(s, cv2.COLOR_GRAY2RGB))

    @staticmethod
    def cartoon(im):
        a = np.array(im.convert("RGB"))
        g = cv2.medianBlur(cv2.cvtColor(a, cv2.COLOR_RGB2GRAY), 5)
        e = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)
        return Image.fromarray(cv2.bitwise_and(cv2.bilateralFilter(a, 9, 300, 300), a, mask=e))

    @staticmethod
    def emboss(im): return im.convert("RGB").filter(PILFilter.EMBOSS)

    @staticmethod
    def sharpen(im): return ImageEnhance.Sharpness(im.convert("RGB")).enhance(3.)

    @staticmethod
    def oil(im):
        return Image.fromarray(cv2.medianBlur(cv2.bilateralFilter(np.array(im.convert("RGB")), 9, 150, 150), 3))

    @staticmethod
    def sobel(im):
        g = cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2GRAY).astype(np.float32)
        m = np.sqrt(cv2.Sobel(g, cv2.CV_64F, 1, 0, ksize=3)**2 + cv2.Sobel(g, cv2.CV_64F, 0, 1, ksize=3)**2)
        mx = m.max()
        return Image.fromarray(cv2.cvtColor(np.clip(m / mx * 255 if mx > 0 else 0, 0, 255).astype(np.uint8), cv2.COLOR_GRAY2RGB))

    @staticmethod
    def pixelate(im, size=8):
        a = np.array(im.convert("RGB"))
        h, w = a.shape[:2]
        sm = cv2.resize(a, (w // size, h // size), interpolation=cv2.INTER_LINEAR)
        return Image.fromarray(cv2.resize(sm, (w, h), interpolation=cv2.INTER_NEAREST))

    @staticmethod
    def invert(im): return ImageOps.invert(im.convert("RGB"))

    @staticmethod
    def posterize(im, bits=4): return ImageOps.posterize(im.convert("RGB"), bits)

    @staticmethod
    def solarize(im, thresh=128): return ImageOps.solarize(im.convert("RGB"), thresh)

    @staticmethod
    def edge_enhance(im): return im.convert("RGB").filter(PILFilter.EDGE_ENHANCE_MORE)

    @staticmethod
    def blur(im): return im.convert("RGB").filter(PILFilter.GaussianBlur(radius=5))

    @staticmethod
    def detail(im): return im.convert("RGB").filter(PILFilter.DETAIL)

    @staticmethod
    def contour(im):
        a = cv2.Canny(cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2GRAY), 30, 100)
        return Image.fromarray(cv2.cvtColor(255 - a, cv2.COLOR_GRAY2RGB))

    @staticmethod
    def thermal(im):
        a = cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2GRAY)
        return Image.fromarray(cv2.applyColorMap(a, cv2.COLORMAP_INFERNO))


FILTER_CHOICES = [
    "Colorize (DeOldify)", "Monochrome", "Sepia", "Film Photo",
    "Canny Edges", "Sobel Edges", "Contour", "Pencil Sketch",
    "Cartoonify", "Oil Painting", "Pixelate", "Blur",
    "Emboss", "Edge Enhance", "Sharpen", "Detail",
    "Invert", "Posterize", "Solarize", "Thermal",
    "Super Resolution (4x)", "Face Restoration",
]


# ============================================================================
# Processor — Orchestrates filter dispatch & resolution management
# ============================================================================

class PhotoProcessor:
    def __init__(self):
        self.colorizer = Colorizer()
        self.sr = SuperResolution()
        self.fr = FaceRestoration()
        self.ready = False

    def init(self):
        if not self.ready:
            self.colorizer.init()
            self.ready = True

    @staticmethod
    def _resize(im: Image.Image, r: int) -> Image.Image:
        w, h = im.size
        mx = max(w, h)
        if mx <= r:
            return im
        return im.resize((r, int(h * r / w)) if w >= h else (int(w * r / h), r), Image.LANCZOS)

    def process(self, im: Image.Image | None, flt: str = "Colorize (DeOldify)", res: int = 1024, fr_weight: float = 0.5) -> Image.Image | None:
        if im is None:
            return None
        self.init()
        d = {
            "Colorize (DeOldify)": lambda i: self.colorizer.colorize(np.array(i.convert("RGB"))),
            "Monochrome": PhotoFilters.mono, "Sepia": PhotoFilters.sepia,
            "Film Photo": PhotoFilters.film,
            "Canny Edges": lambda i: PhotoFilters.canny(i, 50, 150),
            "Sobel Edges": PhotoFilters.sobel, "Contour": PhotoFilters.contour,
            "Pencil Sketch": PhotoFilters.pencil, "Cartoonify": PhotoFilters.cartoon,
            "Oil Painting": PhotoFilters.oil, "Pixelate": PhotoFilters.pixelate,
            "Blur": PhotoFilters.blur, "Emboss": PhotoFilters.emboss,
            "Edge Enhance": PhotoFilters.edge_enhance, "Sharpen": PhotoFilters.sharpen,
            "Detail": PhotoFilters.detail, "Invert": PhotoFilters.invert,
            "Posterize": PhotoFilters.posterize, "Solarize": PhotoFilters.solarize,
            "Thermal": PhotoFilters.thermal,
            "Super Resolution (4x)": lambda i: Image.fromarray(self.sr.upscale(np.array(i.convert("RGB")))),
            "Face Restoration": lambda i: Image.fromarray(self.fr.restore(np.array(i.convert("RGB")), weight=fr_weight)),
        }
        r = d.get(flt, d["Colorize (DeOldify)"])(im.convert("RGB"))
        return self._resize(Image.fromarray(r) if isinstance(r, np.ndarray) else r, res)
