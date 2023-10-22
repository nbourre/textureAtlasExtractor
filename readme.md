# Intro
I created this script because some Kenney assets are in TextureAtlas format and I want to use them in my game. Godot does not have a native support for TextureAtlas files. I have to extract the individual sprite images from the TextureAtlas files.

The format of Kenney's TextureAtlas files is similar to the format of TexturePacker's TextureAtlas files.

# Usage
```bash
python textureAtlas2files.py xml_file atlas_image output_dir
```