# About
This tool (originally made by coynem, go check him out) is used to import pictures into Dreams by converting them into audio. I've modified the original a bit to add some convenience. (config is saved to a file, more supported file formats)

# Usage

### Creating audio

* Install dependencies
```
pip install -r requirements.txt
```

* Put any pictures you want to import into the `Pictures` directory. This is the only place it looks as of now, but I may change that later. 
* Run `Picture Encoder.py`
* Follow instructions printed in console

### Importing image

* Create a new scene with the image importer logic inside
* Open your browser to the [Audio Importer](https://indreams.me/import/audio)
* Import the seperate chunks of audio generated in the `Chunks (___)` subfolders
* Put each audio segment into its appropriate color timeline
* Bake all emitted objects once image is finished printing
* Merge pixels into one painting
* Save painting as new creation (optional)
## Notes

Configuration can be edited in `config.ini`
