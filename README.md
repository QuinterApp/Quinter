# Quinter

Quinter is a light-weight, robust, accessible Twitter client for Mac and Windows.

## Note.

I have stepped back from Quinter development. It was fun while it lasted, but the code is a mess, and a rewrite isn't work I'm willing to do. That said, I'll still check this repo for open Pull Requests, and merge them. I'm honestly not sure if GitHub let's contributors build releases, but if so, feel free once features get merged.

## Running

```batch
git clone https://github.com/QuinterApp/Quinter
cd quinter
pip install -r requirements.txt
run.bat
```

## Building

```batch
git clone https://github.com/QuinterApp/Quinter
cd quinter
pip install -r requirements.txt
build.bat
copy.bat
```

## Contributing.

We ask that pull requests are submitted always, in order to avoid merge conflicts. In addition, if you have a big feature request/idea, it would be better if an issue is opened first, so we can discuss implementation, details, documentation, etc.

## Todo

* Add a timeline-specific find feature.
* Add bookmarks.
* Add shortcut keys for jumping to timelines
* Relative times
	* This won't be possible with our current listview, but maybe in invisible?
* Export buffers feature
* View blocked and muted users.
* add command line arguments for external player
