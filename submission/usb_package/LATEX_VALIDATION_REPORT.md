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

The slide text now uses fenced display math:

```math
|\Psi_i(t)\rangle =
e^{-iHt}
\left(
|\psi_i\rangle_M \otimes |0\rangle_F
\right)
```

```math
|\phi_{i,m}(t,b)\rangle =
\frac{
(I_M \otimes \langle b_m|)
|\Psi_i(t)\rangle
}{
\sqrt{p_{i,m}}
}
```

```math
p_{i,m}
=
\left\|
(I_M \otimes \langle b_m|)
|\Psi_i(t)\rangle
\right\|^2
```

## Remaining Suspicious Patterns

- No broken notebook equation fragments remain.
- No remaining raw measurement-bra presentation Markdown fragments are expected.
- `PRESENTATION_STORYBOARD_EN.md` contains no raw bra-ket equation block.
