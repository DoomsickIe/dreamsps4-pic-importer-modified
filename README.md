# About
This tool (originally made by coynem, go check him out) is used to import pictures into Dreams by converting them into audio. I've modified the original a bit to add some convenience. (config is saved to a file, more supported file formats)

# Usage

### Creating audio

* Install dependencies
```
pip install -r requirements.txt
```

* Run `Picture Encoder.py`
* Specify input image by passing a path
* Tweak settings until you are happy
* Click `export` and wait for it to finish; folders will be created with segments of the output made for importing

### Importing image

* Create a new scene with the image importer logic inside
* Open your browser to the [Audio Importer](https://indreams.me/import/audio)
* Import the seperate chunks of audio generated in the `Chunks (___)` subfolders
* Put each audio segment into its appropriate color timeline
* Bake all emitted objects once image is finished printing
* Merge pixels into one painting
* Save painting as new creation (optional)
