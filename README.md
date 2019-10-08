# Deplocator
A small tool that finds the Maven dependencies for a given set of Java source files by analyzing its import declarations.

## Running
`python3 -m deplocator [project folder] [project package prefix]`

For example, if you have a repository called `myapp` in your current directory with classes being located under `com.myapp`, you can use:

`python3 -m deplocator myapp com.myapp`
