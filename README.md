# test-amplify
Amplify Competency Test

## Use Python to write a program that solves the problem below:

Family Tree Question: this puzzle centers on a family tree.

This test is typically completed in 30 to 40 minutes
We give you longer to allow for interruptions
We do not need you to already have the answer in your head
Doing research is OK

The family tree includes only the first names of female members of the
family, mothers and daughters, through many generations.

Write a function that takes three parameters:

   1. A string representing the family tree
   2. The name of the first person
   3. The name of another person

To keep things simple all names are unique, each name appears only
once in the tree. The tree (parameter 1) is a string form of a
dictionary (hash) where the keys are the names of mothers and the
values are a list of names of their daughters.

For example:
Ann is the root of the tree and has two daughters Betty & Clare.
Betty has three daughters Donna, Elizabeth & Flora
Clare has two daughters Gloria and Hazel.

This could be represented by the string:

    {"Ann": ["Betty", "Clare"], "Betty": ["Donna", "Elizabeth", "Flora"], "Clare": ["Gloria", "Hazel"]}

There are no great granddaughters in this example, so Donna, Elizabeth, Flora, Gloria & Hazel do not appear as keys in the map/string.

A visualization of this might be:
    Ann
       Betty
           Donna
           Elizabeth
           Flora
       Clare
           Gloria
           Hazel

The function should return the closest antecedent of the two given names.
The interpretation of antecedent used here may not be what you assume:
If person ‘X’ is the ancestor of person ‘Y’ then return ‘X’ as the result
See the 2nd and 5th examples below.

Here are several examples of different pairs of people and the result for the tree as above:
   1. IN: Hazel & Gloria             OUT: Clare             (they have a direct common mother)
   2. IN: Hazel & Clare              OUT: Clare             (one is the mother of the other)
   3. IN: Hazel & Flora              OUT: Ann                (closest is their grandmother)
   4. IN: Hazel & Betty              OUT: Ann                (the only ancestor in common is Ann)
   5. IN: Hazel & Ann                OUT: Ann                (one is the grandmother of the other)
   6. IN: Hazel & Hazel             OUT: Hazel              (they are the same person - just return that person)


Some of the tests will have exactly this tree, with exactly this
string representation and exactly these pairs of input names which
exactly these expected outputs.

Other tests will have a different (possibly larger) tree.
For other tests, you should not assume that the keys in the dictionary
string are in any particular order.
