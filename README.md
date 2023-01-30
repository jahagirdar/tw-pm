# Installation

```
git clone git@github.com:jahagirdar/tw-pm.git
cd tw-pm
make
```
And then from your browser open `127.0.0.1:8000`

# Development Status: Alpha

# Background aka 'itch' story.

I always found the tiddlywiki based GTD solutions(mgtd, gsd and [Cardo](https://dyumnin.com/Cardo.html) to be amazing. These solutions had a few major problems during regular usage.

1. As the task database increased in size the browser application because slow. Until it was unusable.
2. Each tiddlywiki implementation had a different backend storage mechanism
3. I do most of my work in a terminal and wanted a CLI interface to my task database.
4. My interaction with tasks is via the vimwiki plugin
 
Taskwarrior solves #2 and #3 but does not have a good browser based frontend.

So the options were either to build a CLI to tiddlywiki, & build a plugin for vim+vimwiki or build a great front end for taskwarrior.

For a long time I wanted to learn svelte and recently discovered FastAPI. So guess which itch I decided to scratch.


# Other Itch that I may(or may not) scratch someday

* Integrate taskjuggler tasks to have a single combined visualization
* Add a meeting mode to capture discussions and new AI's
* Do somekind of multiuser hosted frontend where others can see and annotate tasks assigned to them.
