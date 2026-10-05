# Visual Acuity Calculation and Formula Reference

This document details the mathematical formulas used to convert an object's physical size and viewing distance into an equivalent **Snellen Visual Acuity** fraction ($20/x$).

---

## 1. Mathematical Principles

Snellen visual acuity is based on visual angle $\theta$. By standard definition:
* A standard $20/20$ optotype subtends a total visual angle of $5\text{ arcminutes}$ ($5'$) on the eye.
* The denominator $x$ in a $20/x$ acuity rating represents the ratio of the object's subtended angle relative to the $20/20$ standard $5'$ angle.

### Exact Trigonometric Formula

Given:
* $S$ = Object height/size in millimeters ($\text{mm}$)
* $D$ = Distance from observer in feet ($\text{ft}$)

First, convert distance $D$ into millimeters:
$$D_{\text{mm}} = D \times 304.8\text{ mm/ft}$$

The subtended angle $\theta$ in radians is:
$$\theta_{\text{rad}} = 2 \cdot \arctan\left(\frac{S}{2 \cdot D_{\text{mm}}}\right) = 2 \cdot \arctan\left(\frac{S}{609.6 \cdot D}\right)$$

Converting $\theta_{\text{rad}}$ to arcminutes ($\theta_{\text{arcmin}}$):
$$\theta_{\text{arcmin}} = \theta_{\text{rad}} \times \left(\frac{180 \times 60}{\pi}\right) = \left(\frac{21600}{\pi}\right) \cdot \arctan\left(\frac{S}{609.6 \cdot D}\right)$$

Since $20/20$ corresponds to $5'$, the Snellen denominator $x$ is:
$$x = 20 \times \left(\frac{\theta_{\text{arcmin}}}{5'}\right) = 4 \cdot \theta_{\text{arcmin}}$$

Combining into the master exact formula:
$$x = \left(\frac{86400}{\pi}\right) \cdot \arctan\left(\frac{S}{609.6 \cdot D}\right)$$

---

### Small-Angle Approximation Formula

For small angles where $\tan(\theta) \approx \theta$, we can simplify:
$$\arctan\left(\frac{S}{609.6 \cdot D}\right) \approx \frac{S}{609.6 \cdot D}$$

Substituting into the exact formula:
$$x \approx \left(\frac{86400}{609.6 \cdot \pi}\right) \cdot \frac{S}{D} \approx 45.1148 \cdot \frac{S}{D}$$

---

## 2. Quick Reference Equations

| Target Parameter | Approximation Formula |
| :--- | :--- |
| **Snellen Denominator ($x$)** | $x \approx 45.1225 \times \frac{S\text{ (mm)}}{D\text{ (ft)}}$ |
| **Object Size ($S$ in mm)** | $S \approx 0.02216 \times D\text{ (ft)} \times x$ |
| **Distance ($D$ in ft)** | $D \approx \frac{45.1225 \times S\text{ (mm)}}{x}$ |

---

## 3. Python Script Usage

Run `visual_acuity_calculator.py` from your command line:

```bash
python visual_acuity_calculator.py --size 18 --distance 10
```

### Options
* `-s`, `--size`: Object size in millimeters ($\text{mm}$)
* `-d`, `--distance`: Distance to object in feet ($\text{ft}$)
* `-r`, `--round`: (Optional) Round the visual acuity denominator to the nearest integer.