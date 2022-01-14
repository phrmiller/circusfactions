---
title: The Chief Clerk Says She Wants Apples with Her Salad
date: 2021-12-09
categories: business, alcohol, books, alchemy, science
image: images/clerk.jpeg
image_alt_text: A woman standing at a cashier stand.
summary: And while Gregor gushed out these words, hardly knowing what he was saying, he made his way over to the chest of drawers—this was easily done, probably because of the practise he had already had in bed—where he now tried to get himself upright.
---

Command is one of my favorite patterns. Most large programs I write, games or
otherwise, end up using it somewhere. When I've used it in the right place, it's
neatly untangled some really gnarly code. For such a swell pattern, the Gang of
Four has a predictably abstruse description:

> Encapsulate a request as an object, thereby letting users parameterize clients
> with different requests, queue or log requests, and support undoable
> operations.

I think we can all agree that that's a terrible sentence. First of all, it
mangles whatever metaphor it's trying to establish. Outside of the weird world
of software where words can mean anything, a "client" is a *person* -- someone
you do business with. Last I checked, human beings can't be "parameterized".

Then, the rest of that sentence is just a list of stuff you could maybe possibly
use the pattern for. Not very illuminating unless your use case happens to be in
that list. *My* pithy tagline for the Command pattern is:

**A command is a *<span name="latin">reified</span> method call*.**

<aside name="latin">
"Reify" comes from the Latin "res", for "thing", with the English suffix
"&ndash;fy". So it basically means "thingify", which, honestly, would be a more
fun word to use.
</aside>

Both terms mean taking some <span name="reflection">*concept*</span> and turning
it into a piece of *data* -- an object -- that you can stick in a variable, pass
to a function, etc. So by saying the Command pattern is a "reified method call",
what I mean is that it's a method call wrapped in an object.

That sounds a lot like a "callback", "first-class function", "function pointer",
"closure", or "partially applied function" depending on which language you're
coming from, and indeed those are all in the same ballpark. The Gang of Four
later says:

> Commands are an object-oriented replacement for callbacks.

That would be a better slugline for the pattern than the one they chose.

But all of this is abstract and nebulous. I like to start chapters with
something concrete, and I blew that. To make up for it, from here on out it's
all examples where commands are a brilliant fit.
