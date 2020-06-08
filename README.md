# Zauth4
A user-management system designed for easy Python implementation

# What is Zauth4?

  Zauth is a simple user-management system designed to be secure and easy to implement across all your python applications.
  Allowing users to only have one account across your entire application suite.
  
# History and Development

  Development for Zauth began in 2017 with Zauth Version 1. The idea was to design a free, open-source, easy-to-implement user management platform similar to OAuth. 
  The first design, completed within a few weeks consisted of a simple key system that allowed applications to be registered to a token. However, no other implementation was done, and all processing was done CLIENT side.
  In Zauth 2 and Zauth 3, many thing changed, including implementing Zauth Keyfiles, filehashing, and double-encryption. However, the processing was still done through the client. This was a significant security concern, and it was decided to pull the old versions out of release and work on the new Server-based Zauth 4. Another reason was that it was discovered that any application could use Zauth's internal methods to return the user's password in plain-text. Obviously, this was a HUGE issue that Zauth4 stived to fix.
  
Moving forward to this release of Zauth4. You might notice, it's not functional. Well, not entirely. Zauth4 has fixed the internal method issue, now implementing clever security checks by watching who tried to call protected methods. However, the code is still based on the older Zauth 3 engine with a server layer added, meaning that the server and client are extremely difficult to program for. This is made worse by the failed attempt at RSA encryption, the current Server is broken.

# Discontinuation

It was decided after 3 years of development, I am discontinuing Zauth in favor of a Java-based platform called EZAuth. EZAuth will be what ZAuth should have been. This started as a project for a project, EZNext that I was contracted to develop the server for.

# Public Release

I have decided to make all of the code open for the public to modify and fix. If anyone would like to use this base, or even part of it, I give my complete permission to do so. It is just a lot for me to do at the moment and it's just become a headache to work with.

# Support

I do not provide support for this project any more. I am willing to provide all of my old versions of Zauth, or any other resoureces I can provide by request, but I will not be an exclusive developer any longer.
