# finding_the_wumpus
Finding the wumpus. Implementing the core logic of a knowledge-based agent that knows about the world and extends his knowledge through logic

It's a program that illustrates the core concepts studied in the "Agents that reason logically"  chapter in "Artificial Intelligence - A Modern Approach" (Studar J. Russell and Peter Norvig").

It uses the same example in the chapter about a legacy computer game called wumpus, where an agent explores a cave consisting of rooms connected by passageways. Lurking somewhere in the cave is the wumpus, a beast that eats anyone who enters its room. Some rooms contain bottomless pits that trap anyone who wanders into these rooms (except for the wumpus, who is too big to fall in). The only mitigation feature of living in this environment is the occasional heap of gold. 

There's this 4x4 matrix world where we start from location (1,1).
In the square containing the wumpus and directly adjacent squares, the agent will perceive a stench.
In the squares directly adjacent to a pit, the agent will perceive a breeze.

I will skip the details that are described very nicely in the chapter to the point where they demonstrate how the agent infers from the knowledge that he gathered so far about the world and get to the conclusion that there's a wumpus in (3,1)

The program is provided with the knwoledge gathered so far:
~S1,1 - no stench in (1,1)
~S2,1 - no stench in (2,1)
S1,2 - stench in (1,2)
~B1,1 - no Breeze in (1,1)
B2,1 - Breeze in (2,1)
~B1,2 - No Breeze in 1,2

and some game rules - 

R1: ~S1,1 -> ~W1,1 & ~W1,2 & ~W2,1  -- if there's no stench in (1,1) then there's no Wumpus in the adjacent rooms
R2: ~S2,1 -> ~W1,1 & ~W2,1 & ~W2,2 & ~W3,1 -- if there's no stench in (1,1) then there's no wumpus in the adjacent rooms
R3: ~S1,2 -> ~W1,1 & ~W1,2 & ~w2,2 | ~W1,3 -- if there's no stench in (1,2) then there's no wumpus in the adjacent rooms
R4: S1,2 -> W1,3 | W1,2 | W2,2 | W1,1 -- if there's stenchh in (1,2) then there's a wumpus in one of the adjacent rooms

The agent adds these ten items of knowledge to his database (KB) and then infers and adds new knowledge items to the database. This specific implementation uses modus ponens, and-elimination, and resolution.
