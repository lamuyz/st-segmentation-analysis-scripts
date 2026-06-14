# Spateo Watershed Command Notes

This file records the main commands used for Spateo watershed segmentation and label expansion.

Spateo was run on individual datasets from the command line or interactive Python session, rather than through a unified batch script.

## Watershed Segmentation

```python
# 1. Identify signal regions from the staining image
st.cs.mask_nuclei_from_stain(adata)

# 2. Find peak points for watershed segmentation
# A larger value may reduce over-segmentation.
# A smaller value may help separate touching cells.
st.cs.find_peaks_from_mask(adata, "stain", 7)

# 3. Run watershed segmentation
st.cs.watershed(
    adata,
    "stain",
    5,
    out_layer="watershed_labels",
)

# 4. Visualize segmentation labels over the staining image
fig, ax = st.pl.imshow(adata, "stain", save_show_or_return="return")
st.pl.imshow(
    adata,
    "watershed_labels",
    labels=True,
    alpha=0.5,
    ax=ax,
)
plt.title("Watershed Segmentation Result")
plt.show()
```

## Label Expansion

```python
start_time = time.time()

st.cs.expand_labels(
    adata,
    "watershed",
    distance=EXPAND_DISTANCE,
    max_area=EXPAND_MAX_AREA,
    out_layer="watershed_labels_expanded",
)

expanded_labels = adata.layers["watershed_labels_expanded"].astype(np.uint32)
tifffile.imwrite(EXPANDED_MASK_PATH, expanded_labels)

print("Expanded mask saved to:", EXPANDED_MASK_PATH)
print("max expanded label:", int(expanded_labels.max()))
print(f"Expansion finished in {time.time() - start_time:.1f}s")
```

## Notes

* `find_peaks_from_mask(..., 7)` was used for peak detection.
* `watershed(..., 5)` was used for the watershed step.
* `expand_labels` was used to generate the expanded watershed mask.
* `EXPAND_DISTANCE`, `EXPAND_MAX_AREA`, and `EXPANDED_MASK_PATH` were set according to each dataset.
* Complete input files, intermediate objects, masks, and logs are not stored in this repository.
