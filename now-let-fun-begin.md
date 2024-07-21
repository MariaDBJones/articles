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

Now, let's shift our focus to relationships, which should be represented by tables containing pairs of primary keys (PKs). Technically, we can distinguish three types of relationships: one-to-one (1:1), one-to-many (1:n), and many-to-many (n:n).

While there isn't much that can be done about many to many (n:n) relationships in terms of optimization, there are straightforward ways to optimize one to one (1:1) and one to many (1:n) relationships.

For 1:n relationships, the approach is to store the primary key from the "one" side in a column on the "many" side table. For example, consider a scenario with clients and their addresses. Each address belongs to only one client, but a client can have multiple addresses. In this case, the relationship would be represented by adding a column containing the client's primary key in the address table.

The same approach applies to 1:1 relationships. For instance, a SIM card is linked to a single phone number, but the number can theoretically be reassigned to a different SIM card. This relationship could be represented by adding a column in the phone line table containing the primary key of the SIM card.


#### The strange case of Dr relation and Mister constraint

In database design, foreign keys exhibit a dual nature akin to the characters in "The Strange Case of Dr. Jekyll and Mr. Hyde." Dr. Relation represents the role of establishing meaningful connections between tables, reflecting real-world associations and enhancing the logical structure of the database. He ensures that related entities are accurately modeled, facilitating effective data querying.

On the other hand, Mr. Constraint embodies the enforcement of data integrity. He enforces rules to maintain referential integrity, preventing anomalies such as orphan records and ensuring consistency across tables. Mr. Constraint manages cascading actions to align changes in one table with related data in another.

Together, Dr. Relation and Mr. Constraint ensure that a database is both well-structured and reliable, balancing the creation of logical connections with the enforcement of data consistency and integrity. Many would say that their interplay is essential for maintaining a robust and accurate relational database system. I disagree with this view and firmly believe constraintrs should be upheld in the app layers and that only the relations should be materialized in a database.
But this is a strictly personal view and i will develop the why, pros and cons in a separate article ( yes you read that right, a whole article on that topic alone).

Here comes the end of this third article on how to design a relational schema bringing sustainability, evolutivity and performance tp the table.

Next chapter will focus on the relation between attributes, data types and performance.
