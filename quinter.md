# Quinter

Welcome to Quinter!

## What is Quinter?

Quinter is a fully accessible, easy-to-use, light-weight Twitter client.

## Interfaces

Quinter has two interfaces. GUI and invisible. Invisible allows you to control Quinter from anywhere on your computer. This is disabled by default, but can be easily enabled in settings. GUI allows you to control Quinter like any other application, with buttons, lists, menus, etc.

## Keys.

### GUI

You can find out what keys perform what actions by reading through all of the menu options. For example. Reply (Control+R) or command+r on mac.

### Invisible: 

Here are the default keys for the invisible interface on Windows only, as it does not work on Mac. These keys can be easily remapped by editing keymap.keymap.

* Control+Windows+Shift+T: Show or hide the window. Note: This works even if invisible interface is not enabled.
* Control+Windows+T: Send a tweet.
* Alt+Windows+left arrow: Previous timeline
* Alt+Windows+right Arrow: Next Timeline.
* Alt+Windows+Up Arrow: Previous Buffer item.
* Alt+Windows+Down Arrow: Next buffer item.
* Control+Windows+r: Reply to a tweet.
* Control+Windows+Shift+r: Send a retweet.
* Alt+Windows+L: Like or unlike a tweet.
* Alt+Windows+Q: Quote a Tweet.
* Alt+Windows+Control+D: Send a direct message.
* Alt+Windows+C: Open a conversation.
* Alt+Windows+V: Open the Tweet Viewer
* Alt+Windows+Control+Up Arrow: Increase volume.
* Alt+Windows+Control+Down Arrow: Turn down the volume.
* Alt+Windows+Enter: Open a URL
* shift+windows+alt+enter: Play audio in tweet.
* control+windows+alt+enter: Play audio in tweet using external media player. Note: You must set the media player up in the options dialog first.
* Alt+Windows+Semi Colon: Speak a brief profile overview.
* Alt+Windows+Shift+Semi Colon: Speak what a tweet is in reply to.
* Alt+Windows+Page Up: Load previous items.
* Alt+Windows+U: Open a user's timeline
* Alt+Windows+Shift+U: Open a user's profile.
* Alt+Windows+Tick: Destroy a timeline.
* Alt+Windows+Control+U: Refresh.
* Alt+Windows+Home: Go to the top of the buffer.
* Alt+Windows+End: Go to the end of the buffer.
* Alt+Windows+Delete: Delete a tweet.
* Alt+Windows+Shift+Q: Exit the program.
* Alt+Windows+Left Bracket: View followers.
* Alt+Windows+Right bracket: View Friends.
* alt+windows+o: Options
* control+alt+windows+o: account Options
* alt+windows+shift+left: previous tweet from same user
* alt+windows+shift+right: next tweet from same user
* alt+windows+shift+up: previous tweet in thread
* alt+windows+shift+down: next tweet in thread
* Control+Windows+Shift+C: Copy the last tweet to the clipboard.
* alt+windows+a: Add user to a list
* alt+windows+shift+a: Remove user from a list.
* alt+windows+control+l: View your lists.
* alt+windows+slash: Perform a twitter search.
* Control+Windows+A: Open the account manager.
* Alt+windows+space: Repeat currently focused item.
* Alt+windows+control+a: Speak the current account.
* alt + windows + control + shift + enter: open URL to tweet in browser.
* alt + windows + e: Toggle autoread for current timeline.
* alt + windows + M: Toggle mute for current timeline.

## Templates.

Quinter supports a template system, allowing you to choose what information you want shown when viewing tweets, direct messages, retweets, etc. Each bit of information goes between two dollar signs ($), and you can have other symbols outside of the dollar signs. The possible objects are as follows: 

### Tweets: , retweets, and quotes.

* user.screen_name: The @HANDLE of the user.
* user.name: The display name of the user.
* text: The text of the tweet.
* created_at: The timestamp of when the item was created.
* source: The client it was sent from.
* retweet_count: The number of retweets.
* favorite_count: The likes count
* possibly_sensitive: Is this tweet marked as possibly containing sensative content?
* lang: The language of the Tweet

### Direct Messages: 

* sender.screen_name: The @HANDLE of the user that sent the message.
* sender.name: The display name of the user that sent the message.
* recipient.screen_name: The @HANDLE of the user the message was sent to.
* recipient.name: The display name of the user that received the message.
* text: The text of the message.
* created_at: The timestamp of when the item was created.

### Users

* name: The display name of the user.
* screen_name: the @HANDLE of the user
* followers_count: The amount of followers the user has.
* friends_count: The number of friends the user has.
* statuses_count: The number of tweets sent by the user.
* description: The user's bio.

## Options

Quinter has two different options dialogs. One is for global settings that apply across the hole app. The other is for the currently selected account.

### Global options

This dialog is divided into multiple tabs. They are as follows.

* General: General options, such as ask before dismissing timelines.
* Templates: Template settings.
* Advanced: Options that are exparamental, or could possibly break the app if not used propperly.

#### General

* Ask before dismissing timelines: If checked, this will show a warning message when destroying timelines.
* Play a sound when a tweet contains audio that is playable by either the client or an external media player: If checked, this option will make Quinter make a sound if you come across a tweet with playable media.
* Play a sound when you navigate to a timeline that may have new items: This option will play a sound if a timeline you navigate to has items that might be new (i.e. you're not at the edge of the timeline).
* Remove emojis and other unicode characters from display names: Tired of people with 50 emojis in their names? Check this box, and suffer no more! If the user in questoin has only emojis, the screen name will show instead.
* Remove emojis and other unicode characters from tweet text: This option is similar to the username one, but it works with tweet text.
* Reverse timelines (newest on bottom): This option puts the newest tweets at the bottom, rather than at the top.
* Word wrap in text fields: If checked, long lines will wrap onto new lines in any text field, including the new tweet dialog.
* when getting URLs from a tweet, automatically open the first URL if it is the only one : If a tweet contains only one URL, pressing the open URL command will open it by default if this is checked.

#### templates.

* Tweet template: Customizehow standard tweets and replies are displayed.
* Quote template: Customize how quotes are displayed.
* Retweet template: Customize how your retweets are shown.
* Copy template: Customize what data gets coppied when you copy a tweet to your clipboard.
* Direct message template: Customize how your DM's are shown.
* User template: Customize what info is shown in user summaries.

#### Advanced

* Enable invisible interface (exparimental): Enables the global hotkeys.
* Sync invisible interface with UI (uncheck for reduced lag in invisible interface): If unchecked, this optoin aims to way improve performance in the invisible interface.
* Repeat items at edges of invisible interface: If this is checked, when you hit an edge in the invisible interface, it will repeat.
* Speak position information when navigating between timelines of invisible interface and switching timelines: If checked, you will be told how far down a timeline you are when navigating to it.
* Update time (in minutes): This changes how frequently the API tries to pull for new tweets.
* Max API calls when fetching users in user viewer: This changes how many followers and friends you can pull when viewing them. One request = 200 followers/friends.
* Number of tweets to fetch per call (Maximum is 200): Changes how many tweets you pull per request (mainly noticeable on startup).
* Enable streaming for home, mentions, and list timelines (This is very experimental! Requires restart to disable): Enables very, very exparamental and breaky streaming API support.
* External media player. You can choose your media player of choice here.

### Account options.

This dialog doesn't currently contain much, and currently only contains the following tabs:

* General: General options.

#### General.

* Soundpacks: Let's you choose your soundpack.
* Sound pan: This allows you to pan account-specific sounds to a different position in the stereo field, so you don't have to use different sound packs for different accounts.
* Tweet Footer (optional): This allows you to automatically append some text to the end of your tweets. Like a hashtag if tweeting about an event.

## Project links.

[Source code](http://github.com/masonasons/quinter)
[Main website](http://masonasons.me/pages/quinter.php)

Enjoy!
