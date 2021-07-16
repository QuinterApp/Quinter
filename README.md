# Quinter

Quinter is a light-weight, robust, accessible Twitter client for Mac and Windows.

## Running

```batch
git clone http://github.com/masonasons/quinter
cd quinter
pip install -r requirements.txt
run
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
* Play the buffer edge sound when going through threads/user-specific tweets and reaching the edge.
* Let you customize how much Control+Windows+Page up/down moves you (within reason of course).
* Fix the problem where empty timelines actually let you somehow scroll through them.
