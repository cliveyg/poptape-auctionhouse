# poptape-auctionhouse
![Unit tests](https://github.com/cliveyg/poptape-auctionhouse/actions/workflows/unit-test.yml/badge.svg) ![Successfully deployed](https://github.com/cliveyg/poptape-auctionhouse/actions/workflows/post-merge-deployment.yml/badge.svg) ![Tests passed](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cliveyg/d99b55c1eeb7ed01c7c81072b66b6cfb/raw/e9d3675138193249fdc08d5f358867a49ef76329/poptape-auctionhouse-junit-tests.json&label=Tests) ![Test coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/cliveyg/d99b55c1eeb7ed01c7c81072b66b6cfb/raw/b0bcda3d043644c7f7a7a5c28789bc24156e653f/poptape-auctionhouse-cobertura-coverage.json&label=Test%20coverage)

A microservice written in Python Django that controls auctions, i.e. create,
delete, update an auction with items or lots and start times etc. Also in this
microservice are items or lots but I may spin this out into a seperate micro-
service in the future.

Please see [this gist](https://gist.github.com/cliveyg/cf77c295e18156ba74cda46949231d69) to see how this microservice works as part of the auction system software.

I've made various design decisions that I may change such as that an item can
appear in more than one auction and have different prices in different auctions.
It may turn out to be better to make items unique to an auction with only one 
price. An item or lot can only be in one live auction at a time. 

I'm also unsure of my choice for model design. I think having an auction lot 
base class and then various child classes based on auction type works but again
I may revisit this. It's a bit odd having auction type hanging off auction item
but it's not strictly an auction type but valid fields for a lot or item based
on auction type. naming stuff is hard :)

There are many different auction types but I'm going to provide the following
types of auctions:
* English
* Dutch
* Sealed bid
* Vickery
* Reverse
* Bidding fee
* Buy it now
* Make me an offer

See [Wikipedia](https://en.wikipedia.org/wiki/Online_auction) for more info
on auction types.

I'm also planning that this application can be used in live auctions in auction
houses.

##### Note:
This microservice is only partially working. Extremely early alpha version.

##### API Routes:

```
Coming soon...

```

------

##### Testing:

Some model testing done. Need to complete the rest.

------

##### TODO:
* All of it!
