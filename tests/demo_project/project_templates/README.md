Thought the right place to put the project templates would be
the "project app" (that is, the app that holds the settings file)

It is not uncommon for a non-app template directory to exist.
Such directory gets picked up the filesystem.Loader instead of 
the app_directories.Loader.

In order to properly test template loading / rendering features,
we need to supply our test project with such a directory.

That is, this directory exists in order to be able to test against
the filesystem.Loader
