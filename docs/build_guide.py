# -*- coding: utf-8 -*-
"""
Build script to generate the comprehensive Learning, Demo, and Oral Defense Guide
for ContainerLab (Virtualisation & Cloud Computing, ESSTHS).
Generates:
1. docs/guide-apprentissage-soutenance.md (Markdown)
2. docs/guide-apprentissage-soutenance.html (Self-contained HTML with embedded base64 images & print CSS)
3. C:\Users\houss\Desktop\ContainerLab_Guide_Apprentissage_Soutenance.pdf (Compiled PDF via Edge headless)
"""

import os
import sys
import base64
import subprocess

print("Initializing guide generator...")
