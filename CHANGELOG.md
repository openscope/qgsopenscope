- [Pre-releases](#pre-releases)

# Pre-releases

## 0.0.7-alpha1 (January 22, 2020)
## Bugfixes
- Fix DEM file fetching for Southern Hemisphere and handle non-standard tile regions (eg. Svalbard)
- Fix test for empty geometry when exporting video maps
- Fix zooming to airspace extents when loading an airport or generating terrain

## New Features
- Allow drawing of circles with a decimal radius (min 0.005 NM, ~ 10 m)

## 0.0.6-alpha3 (January 16, 2020)
### Hotfixes
- Handle raster layer when getting features
- Test for empty geometry

### New Features
- Add Import Airport Dialog, which allows which items to be imported
- Add Export Terrain Dialog, which provides a list of which terrain layers can be exported
- Add WDBII Rivers (Levels 1-3)
- Add OpenStreetMap layer to the project
- Improve coordinate validation

## 0.0.5-alpha1 (November 5, 2019)
### New Features
- Add setting for where the project files are saved
- Save the project file
- Save the water and contour files

### Enhancements & Refactors
- Optimise contour generation
- Don't load the existing terrain by default

## 0.0.4-alpha1 (October 8, 2019)
### Enhancements & Refactors
- Load existing terrain file as read-only, if found
- Update icons
- Improve error handling

## 0.0.3-alpha2 (October 4, 2019)
### Enhancements & Refactors
- Separate out terrain generation

## 0.0.1-alpha1 (September 18, 2019)
- Initial release
