# pkg-unpack

Patches nodejs apps packed using vercel pkg to make 
them dump code. Might be broken for new versions of 
pkg.

Note: there's an attempt to prevent execution, but
you're still executing a random binary. beware.

Usage: `python3 patch.py [path/to/binary]`
