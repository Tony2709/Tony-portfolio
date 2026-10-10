# Brand system PDFs

`build-brand-docs.py` turns the project brand documents (brand context, brand voice,
ideal customer profile) into one branded PDF per project, written to
`public/docs/`.

Run it from the project root when the source documents change:

```bash
python3 scripts/build-brand-docs.py
```

Source documents live outside this repo, on Tony's machine:

- MJ Health: `~/Desktop/EXES SUBJECT/MJ-HealthNutritionFitness/_context/`
- Panther Fit: `~/Desktop/Panther Fit/Context/`

The PDFs themselves are committed, so the site builds without the sources present.
