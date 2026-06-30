# LaTeX / Bra-Ket Validation Report

## Broken Expressions Found

The audit found raw plain-text bra-ket equations in:

- `solution/solution_1.ipynb`
- `submission/usb_package/source_code/solution/solution_1.ipynb`
- `submission/usb_package/presentation/PRESENTATION_SLIDE_TEXT_EN.md`

The problematic fragments were raw ASCII ket equations using `tensor` text,
ASCII `>` ket endings, and unescaped measurement bras in Markdown.

## Expressions Fixed

The final notebook and USB notebook now use display LaTeX for:

```text
|\Psi_i(t)\rangle =
e^{-iHt}
\left(
|\psi_i\rangle_M \otimes |0\rangle_F
\right)
```

```text
|\phi_{i,m}(t,b)\rangle =
\frac{
(I_M \otimes \langle b_m|)
|\Psi_i(t)\rangle
}{
\sqrt{p_{i,m}}
}
```

```text
p_{i,m}
=
\left\|
(I_M \otimes \langle b_m|)
|\Psi_i(t)\rangle
\right\|^2
```

The slide text uses safe plain-text notation inside a fenced `text` code block:

```text
Psi_i(t) = exp(-i H t)(psi_i_M tensor |0>_F)
phi_i,m(t,b) = (I_M tensor <b_m|) Psi_i(t) / sqrt(p_i,m)
p_i,m = ||(I_M tensor <b_m|) Psi_i(t)||^2
```

## Remaining Suspicious Patterns

- No broken notebook equation fragments remain.
- The only remaining `<b_m|` fragments in presentation Markdown are inside a
  fenced `text` block, so Markdown does not interpret them as HTML.
- `PRESENTATION_STORYBOARD_EN.md` contains no raw bra-ket equation block.
