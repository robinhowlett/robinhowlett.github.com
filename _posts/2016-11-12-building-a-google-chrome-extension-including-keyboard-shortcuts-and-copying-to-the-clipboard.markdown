---
layout: post
title: "Building a Google Chrome Extension (Keyboard Shortcuts, Copying to the Clipboard, and Notifications)"
date: 2016-11-12 00:27:43 -0700
comments: true
tags: code chrome snaplogic
---

I recently had the quite enjoyable and productive experience of writing [Pipeline Linker](https://chrome.google.com/webstore/detail/snaplogic-pipeline-linker/cmngkccmjnhnjhjcnmajoiacacnjefgb), my first [Google Chrome Extension](https://www.google.com/chrome/webstore/extensions.html).

As part of my work with [SnapLogic](http://www.snaplogic.com/), an enterprise integration platform-as-a-service (iPaaS) provider, I often have to navigate to Pipelines (hosted graphical representations of integrations) across multiple environments (both internal and customer-facing), client accounts, and project folders.

In turn, as the manager of my team, I regularly direct team members to Pipelines that require attention through email, Hangouts, JIRA, Zendesk, and Slack.

For whatever reason, our product had not provided an easy way of linking directly to these pipelines (you had to switch to a different tab and perform a search, before right-clicking on a table entry and copying the link). 

Over a weekend, I was pleasantly surprised by the ease and speed I was able to learn and implement a Chrome Extension that would address this gap, as well as add some features that I, in particular, value.

![cropped](/assets/images/pipeline-linker-recording.gif)

<!-- more -->

#### How it works

The name of the Chrome Extension is [Pipeline Linker](https://chrome.google.com/webstore/detail/snaplogic-pipeline-linker/cmngkccmjnhnjhjcnmajoiacacnjefgb), and it makes it easier to share links to Pipelines by copying the direct link of the active Pipeline to your clipboard:

> I have open-sourced the extension's code on GitHub: [https://github.com/SnapLogic/pipeline-linker](https://github.com/SnapLogic/pipeline-linker)

When installed, this Chrome Extension will initially be grayed out and disabled:

![installed](/assets/images/NNhY.png)

It will only be enabled if it detects the active tab is the [SnapLogic Designer](https://www.snaplogic.com/features/snaplogic-designer) (regardless of whether it was an internal or external environment):

![enabled](/assets/images/X4su.png)

When one wishes to share the direct link to the currently active pipeline in Designer, the extension's icon beside the Chrome address bar (see above) is clicked or the keyboard shortcut is used (default is `Ctrl+i`. Mac users, it is `control+i`, not `command(⌘)+i`:

When triggered, a Chrome Notification indicates that the Pipeline Link was copied to your clipboard:

![notification](/assets/images/vtlv.png)

The notification message contains the name of the Pipeline, and the smaller contextual message below is the location of the pipeline and the Org name in parentheses.

In your clipboard, a link like the following will be present and ready to be shared:

![slack](/assets/images/MMps.png)

#### Writing the extension

I had a short list of requirements for this extension:

1. It needed to retrieve the rendered HTML of the Designer page so it could be parsed for the information required to build the links.
1. The generated link should be copied to user's clipboard.
1. A notficiation should be given to the user when the link has been copied.
1. The extension could be triggered with a keyboard shortcut.
1. The extension should only be enabled for the SnapLogic Designer.

The [Chrome Extension Developer Documentation](https://developer.chrome.com/extensions/getstarted) is required reading, so I'm assuming the reader has done that. 

For the above requirements, 3 files would comprise the entirety of the functionality needed to cover the above:

* the **[background.js](https://github.com/SnapLogic/pipeline-linker/blob/master/js/background.js)** script, containing the majority of the JavaScript logic for the extension.
* the **[content.js](https://github.com/SnapLogic/pipeline-linker/blob/master/js/content.js****)** script, which is injected into HTML document of the user's current browser tab, and executes the callback function, passing back the page's rendered HTML. This is how the *background.js* file receives the HTML to generate the Pipeline link.
* the **[manifest.json](https://github.com/SnapLogic/pipeline-linker/blob/master/manifest.json)** file, which specifies the browser permissions required, the background scripts, that it is a *page_action* (it applies to a specific page rather than some generic behavior), the image files used as icons, and the keyboard shortcut commands.

**The Manifest**

``` javascript
{
  "name": "SnapLogic Pipeline Linker",
  "description": "Copy the Active Pipeline's Link to the Clipboard",
  "version": "1.0",
  "manifest_version": 2,
  "permissions": [
    "activeTab",
    "notifications",
    "declarativeContent"
  ],
  "background": {
    "scripts": [
      "js/background.js"
    ],
    "persistent": false
  },
  "page_action": {
    "default_icon": {
      "19": "img/icon-19.png",
      "38": "img/icon-38.png"
    },
    "default_title": "Copy the link to the active pipeline"
  },
  "icons": {
    "128": "img/icon-128.png",
    "48": "img/icon-48.png",
    "16": "img/icon-16.png"
  },
  "commands": {
    "_execute_page_action": {
      "description": "Copy the link to the active pipeline",
      "suggested_key": {
        "default": "Ctrl+I",
        "mac": "MacCtrl+I"
      }
    }
  }
}
```

The above manifest is quite simple - most of the properties are self-explanatory, but I'll call out the following that are worth further discussion:

* `permissions` includes `activeTab` (the extension only cares about the tab the user is currently using), `notifications` (for pop-ups), and `declarativeContent` (to use the metadata for the current tab - especially the URL - to control whether the extension is enabled or not). 
	
	The `notifications` permission results in the user being prompted with the following reasonable request when installing the extension:
	
	![installation](/assets/images/5myi.png)
	
	Both `activeTab` and `declarativeContent` have the advantage of not generating any additional permission warnings to the user.

* `background` lists the scripts that run when the extension is active. A single script (`background.js`) is listed. 

	The `"persistent": false` identifies this as an [Event Page](https://developer.chrome.com/extensions/event_pages) - a more performant and efficient solution that allows Chrome to load and unload the extension's scripts automatically, based on the activity of the current page.

* `commands` enables keyboard shortcuts to be defined and configured. When the user performs the shorcut (either using the default, suggested keys or after customising it themselves in their Chrome settings), the reserved [`_execute_page_action`](https://developer.chrome.com/extensions/commands) event is triggered. 

	This event is special in that it doesn't need to be handled - the extension plugin framework takes care of the execution itself.

**Enabling the Extension only for particular pages**

Page actions "represent actions that can be taken on the current page, but that aren't applicable to all pages." Therefore the `pageAction` API was used to add listeners etc.

The `declarativeContent` permission mentioned earlier allows use of the [`chrome.declarativeContent` API](https://developer.chrome.com/extensions/declarativeContent). This API (available since Chrome 33) allows the extension "to take actions depending on the content of a page, without requiring permission to read the page's content."

``` javascript
// only enable the extension on SnapLogic Designer
chrome.runtime.onInstalled.addListener(function () {
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function () {
        chrome.declarativeContent.onPageChanged.addRules([{
            conditions: [
                new chrome.declarativeContent.PageStateMatcher({
                    pageUrl: {hostSuffix: "elastic.snaplogic.com", pathEquals: "/sl/designer.html"},
                })
            ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
        }]);
    });
});
```

The [`chrome.declarativeContent.PageStateMatcher`](https://developer.chrome.com/extensions/declarativeContent#type-PageStateMatcher) allows definiting the `hostSuffix` and `path` that, when matched, enables the extension. When the condition does not match, the extension icon shows us as grayed out and nothing happens when it is clicked:

![enabled-disabled](/assets/images/CKyG.png)

**Parsing the HTML**

The `background.js` script isn't able to access the HTML of the active tab. Instead, another script (`content.js`) is injected into the current page which then communicates with `background.js` by passing messages:

``` javascript
// when the PipelineLinker extension is triggered
chrome.pageAction.onClicked.addListener(function (browserTab) {
    // execute the script that gets injected into page of the current tag
    chrome.tabs.executeScript(null, {file: "js/content.js"}, function () {
        // send a message to content script
        chrome.tabs.sendMessage(browserTab.id, "Background page started.", function (response) {
            // receive the HTML from the tab's page and convert it to a DOM Document
            var doc = htmlToDocument(response);
			...
        });
    });
});

function htmlToDocument(str) {
    // HTML5 <template> allows any element underneath it
    var template = document.createElement("template");
    if (template.content) {
        template.innerHTML = str;
        return template.content;
    }
}
```

To receive the HTML of the target page the extension wishes to interact with, the above code runs as part of the `background.js` script. It adds a listener to the page action that, when triggered, sends a message (using Chrome's [Message Passing API](https://developer.chrome.com/extensions/messaging)) to the `content.js` script. 

The `content.js` script is extremely simple:

``` javascript
chrome.runtime.onMessage.addListener(function (msg, _, sendResponse) {
    sendResponse(document.all[0].outerHTML);
});
```

On receiving the message sent by the `background.js`, it executes the callback function, passing it [the entire HTML (as a String)](http://stackoverflow.com/questions/8853784/get-html-from-a-selected-tab) of the active tab.

The anonymous callback function that was passed in `background.js` then converts that HTML to a Document by using [HTML5's `<template>` element](http://stackoverflow.com/a/35385518/277133), which "allows any other element type as a child".

The [rest of the function](https://github.com/SnapLogic/pipeline-linker/blob/master/js/background.js#L20) is then just using selectors to navigate to the portion of the HTML of interest to the extension to build and copy the link, and the send the browser notification.

**Copying to the Clipboard**

This was surprisingly difficult to identify with Google searches. I tried a few different methods that did not work - it must have been something particular with how `background.js` executes in the context of the Chrome Extension architecture vs the browser. Anyway, I finally [found a function](http://stackoverflow.com/a/18455088/277133) that worked well:

``` javascript
function copyToClipboard(pipelineLink) {
    const input = document.createElement("input");
    input.style.position = "fixed";
    input.style.opacity = 0;
    input.value = pipelineLink;
    document.body.appendChild(input);
    input.select();
    document.execCommand("Copy");
    document.body.removeChild(input);
};
```

**Triggering a Notification**

Again, very straightforward thanks to the [`chrome.notifications API`](https://developer.chrome.com/apps/notifications):

``` javascript
function createNotification(pipelineName, pipelineLocation) {
    var opt = {
        type: "basic",
        title: "Pipeline Link Copied",
        message: pipelineName,
        contextMessage: pipelineLocation,
        iconUrl: "img/icon-80.png"
    };
    chrome.notifications.create(null, opt, function (notificationId) {
        timer = setTimeout(function () {
            chrome.notifications.clear(notificationId);
        }, 3000);
    });
}
```

Being able to control the duration of the popup was a nice extra.

**Keyboard Shortcuts**

Defining a keyboard shortcut is done entirely within the `manifest.json` file:

``` javascript
{
  ...
  "commands": {
    "_execute_page_action": {
      "description": "Copy the link to the active pipeline",
      "suggested_key": {
        "default": "Ctrl+I",
        "mac": "MacCtrl+I"
      }
    }
  }
 }
```

When the user performs the shorcut, the reserved [`_execute_page_action`](https://developer.chrome.com/extensions/commands) event is triggered. The `suggested_key` lists the default and/or OS-specific commands that are bound to the extension out-of-the-box. However, the user can change these to whatever they wish with a link at the bottom their `[chrome://extensions](chrome://extensions/) page:

![chrome-extensions-page](/assets/images/KVH9.png)

There were two "gotchas" worth calling out; on Mac, I couldn't get a command with two or more combinations of Control/Shift/Command keys plus a letter (as per [this SO answer](http://stackoverflow.com/a/18541816/277133)) - hence the default of Ctrl+i. Other responses on that thread appear to have a different experience. 

The other thing to watch out for is when OS-global shortcuts override your selected shortcut combination. My Evernote app had shortcuts defined that were interfering, sometimes silently.

**Final Thoughts**

[Publishing the extension](https://developer.chrome.com/webstore/publish) to the Chrome Web Store was straightforward. A fair number of logo sizes were recommended. My graphical skills are minimal but I was able to knock something out easily enough.

Overall, creating a Chrome Extension is a concise but pleasant development experience and an extremely effective way of distributing "polyfill"-style features for existing web applications.