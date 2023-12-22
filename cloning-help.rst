The common object repository (COR) contains a Vulnerability object for every CVE that was every created, which is over 200,000 entries.  Because it is so large, there 
has sometimes been an issue cloning it.  If you encounter an error similar to this:  

    | fatal: early EOF
    | fatal: index-pack failed

you may be able to use the following command line instructions to perform the cloning.

1. First, turn off compression:

``git config --global core.compression 0``

2. Next, let's do a partial clone to truncate the amount of info coming down:

``git clone --depth 1 <repo_URI>``

3. When that works, go into the new directory and retrieve the rest of the clone:

``git fetch --unshallow``

or, alternately,

``git fetch --depth=2147483647``

4. Now, do a regular pull:

``git pull --all``

5. Reset the compression:

``git config --global core.compression -1``

or, alternatively

``git config --global --unset core.compression``
