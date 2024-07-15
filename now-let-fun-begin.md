# Let the fun begin !!!

No we have defined our facts, their attributes and the relations that unites all those facts. So we're good aren't we ?
Not really. The complete guide to build a good schema can be summlarized as :
"Normalize unitil it breaks, denormalize until it works". Let the fun begin !!!

So what is denormalization ? What is it for ? Sounds like undoing what we did in the first place uh ?

Denormalization is the process of intentionally introducing redundancy into a database by combining tables or adding some degrees of redundancy to optimize read performance. It is often used to improve query performance in read-heavy databases where the cost of frequent joins between normalized tables outweighs the benefits of eliminating redundancy. Balancing the trade-offs between normalized and denormalized structures is key to effective database design. It is in fact the most important skill of a schema designer.

Denormalization helps answering to the following challenges :
1. what about the leftovers aka "bullshit" ?
2. usefull simplifications
3. managing relations

### Managing the leftovers ( aka bullshit )

Leftovers can be cateogrized in two populations : dynamic attributes and technical tokens

Dynamic attributes should not be considered as attributes in the normalisation process given their nature. This being said they are far from useless and can come in very handy for searchability.  Once again age is a very good exampleor indicating this a premium client, or one that has already purchased or cross some significant thresholds in your business. In system having generated column, this is an excellent use case for those. Views can also be used to propose the calculations on top of the reelvant attributes. 

Technical tokens are not attributes of a fact in the sense of a business constraint. Yet they are still attributes of the technical object that represent the fact. So they have to be treatred as such. Good examples are : date of update, user who last updated it, 


### Usefull simplifications

In some cases a strict adherence to normalization will lead to having unecessary informations stored into the database. Let's get back to the exmaple of phone number. While it is definitly not an attribute of the owner, her's how it should be stored : 
facts : human, device, phone line
attributes : phone mline : phone number
relations : possession : linking human and device, attachment : linking device and phone line.

This is only usefull for a phone operator in order to manage its systems.

So for most needs we will either create a phonenumber table or a more global communication table in which we can store mails, phone numbers, social network handles, type them and even indicate the preferred way of being reached out to ( call, mail, text, whatsapp, dm on social networks, etc ).

Same goes for the address. Put it in a separate table and type the different addresses ( mailing, invcoiing, delivery etc )

### Managing relations

on to one ( 1:1)
on to many (1:n)
n:n

The strange case of foreign keys (aka referential integrity contraints ) and integrity constraints

