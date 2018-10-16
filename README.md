# mercari-chain

## Technology Stack
- Node.js
- React
- GraphQL
- MongoDB
- Ethereum

## General Idea
We're tackling the problem of trust for all sharing economy endeavours (relevant themes are Security & Privacy, and Fairness). You generally know if a user is a good or bad actor when they transact a lot on your platform. The problem is telling how a user will behave when they're new, or infrequently use your service. By solving this, we eliminate cases of fraud and have users trust us more.

It's based off a simple idea: if you know a lot of good actors, then you're likely trustworthy. The reverse is true too for knowing bad actors.

The two pieces of information we need are as follows:
1. Knowledge of whether some people are good actors or bad actors (e.g. good sellers on Mercari vs sellers who have a lot of bad reviews)
2. Access to people's list of Facebook friends, and their Facebook identity

Connecting this information as kernels of truth, we'll construct a network-based algorithm that determines whether a person is trustworthy or not based on how many good/bad actors they know.

Here's the cool thing - the database will be constructed by totally independent sharing economy platforms working together. We'll put it on a blockchain to completely decouple it from any particular platform, while giving them all shared ownership of the database and ensuring that they can mutually trust it!

## Sketch of Algorithm
- Identify known people in friends' list 
- If number of known people in friends' list falls short of threshold, return null
- Else just aggregate trustworthiness of known people to generate trustworthiness score for Person X

## Simplified User Stories
### Sally the Good Seller
#### Sally's Perspective
- Sally logs in to Mercari and gets greeted with a message: "connect your Facebook and get a reputation boost!"
- Sally, wanting to be an even better seller with more customers, happily connects her Facebook account, allowing Mercari access to her list of friends.
- Sally gets a reputation boost and a badge that helps people trust her, leading to more sales

#### Under the Hood
- Mercari knows that Sally is a good seller because she has 99% positive transactions on Mercari
- Mercari now has access to Sally's friends list and therefore knows who she knows, and her unique Facebook ID
- Now whenever another user connects their Facebook account, we can trust them more if they know Sally.

### Nancy the New Buyer
#### Nancy's Perspective
- Nancy signs up and gets prompted to connect her Facebook account to help us trust her more
- She gets identified as a good actor and carries on transacting well!

#### Under the Hood
- Mercari now has access to Nancy's friends list and therefore knows who she knows, and her unique Facebook ID
- She connects it. We can tell that she knows Sally the Good Seller and 5 other good actors. She also knows 1 bad actor.
- We do some math based on the quality of actors she knows and reason that she's probably a good actor!
