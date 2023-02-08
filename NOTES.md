Here are my notes, I think they are illustrative of my thought process:


> First thing that stands out to me is that the problem specification indicates that the input will come from stdin, but the code template seems to indicate that it will come from the fileinput.input() function call. It also notes that the java and javascript int parsing functions should be sufficient, but makes no mention of python. Finally the problem statement seems to say "print", which usually means stdout, but then the codeHere function indicates to use the function to return the solution. To me that could mean a test library importing the function, calling it, and cheeking the string return for correctness.
>
> I think I have to assume that the writers of the prompt work in java / javascript and overlooked python. It would be a little ridiculous to use python to make calls to java / javascript just to parse an int. I can handle both stdin / fileinput sources and can also handle both function return / stdout output. This would be something I'd normally briefly confirm with the writer. This is a test situation, so it seems a little pedantic to be thinking of these things. In real life, these misunderstandings can cause significant delays and bugs, so it's usually worth at least quickly checking in.
>
> The prompt indicates that the input will at least be well-formed to the degree that each line will start with the function name and that the arguments will be correctly structured. I'll handle the situation if that isn't true with a fatal error because, at least as written, it seems like a pretty unrecoverable error if that isn't true. I'd rather have the program respond like this over swallowing the error so that testing / observability can catch the very-wrong problem.
>
> The next thought up is considering a solution for the stats call: should I count the initial lines and assign that to one result or should I keep track as the program runs. Again it's potentially a matter of semantics, but the prompt does say "calls", so I think it's appropriate to keep track as the program runs and actual calls are made. Definitely need to watch out for fibonacci potentially being recursive and the tally of calls being made for each fibonacci recursive call instead of the initial fibonacci call. Personally, I don't love recursive calls because I find that they are harder to understand / debug. I tend to lean towards creating the stack in my code rather than relying on the call stack.
>
> Parsing-wise, I like to use a paradigm where it assumes correctness and fails otherwise. I find this is helpful for managing things such as the fatal error. It also makes it a little easier to handle the situations in the calls where maybe some of the inputs are correct, but any of them being wrong invalidates the entire line.
>
> Math-wise, I'm sure that there are some very clever ways of calculating fibonacci and overlapping ranges. I'll spend some time thinking about that, but I may put off that research until the end, like the prompt indicates re:space/time complexity.
>
> My overall goal is to keep the program well-named, well-structured, and simple. It might benefit from allowing easy expansion for new types of functions, but I think there's an appropriate balance between factoring and simplicity. Same situation with classes / function calls: I'm choosing to do direct / static binding because it's just a simpler and easier program to understand. If the writer needs or anticipates more function types being added, then the solution can be reworked to do that, but I think it's wiser to just write the program quick and iterate in the future if needed. That said, I am going to try and make sure I use dependency injection where appropriate because code does have a tendency to evolve and become untestable if side-effects can't be injected.
>
> It's python 3.7.7, which I believe has type hints. Not sure why such a low python minor version is chosen, but I'll refer to the docs for that version. Docs are for 3.7.14, but I'm going to assume that the patch version won't be critical. F-Strings are added in python 3.6, so I'm assuming those will work too. No TypedDicts though, that's unfortunate!
>
> I'm not going to worry about whether or not this module is going to be used as a library and if I should be keeping functions "private". We can work on a consumable interface later if the writer wants it.
>
> Update: fileinput is apparently a great standard library module that handles input from stdin as well as potential files. I assumed that fileinput was a custom module by this testing app. That's great news because now I don't need to handle different input sources. I'm still going to handle the output sources though, but honestly the current program structure looks appropriate for that given the printing of codeHere.
>
> I would also love if this editor supported python type hints. I'm going to write it all out here so that the writers can see the stream of changes, but I will also likely check it in vscode to make sure it's typed correctly.
>
> Thinking about now whether to parse early and add handlers or to return maybe-error types back from the calls. I think it's best to keep the error handling within the fib and overlap calls because it's hard to indicate predicate types without that system in place, so e.g. if the fib function is called independently then it is still a possibility that someone calls it with wrong inputs. It's a bummer though because it pollutes the rest of the code.
>
> At this point I think I have all of my error handling and parsing complete. Now I just need to do the math for fibonacci and overlap. Went back and forth on a few things. Mostly on whether to make individual classes for the different input commands or not. I think since I'm using data classes, it makes more sense to use just one class. A more object-oriented approach would probably see the serialize and calculate functions included, but still having the maybe-args variable. I used the maybe-args paradigm because I'm waiting on the parsing errors until the last moment because I want the calculate functions to handle a broad range of inputs even when called by other code later.
>
> It's also not super clear if fibonacci of 1 should include both 1s or not.
>
> Alrighty- time to test. Good thing this app comes with a tester!


Thank you!
