# How to disintguish facts, attributes and relations from bullshit ?
We've seen in me previous post ( who said rant ? ) how to easily normalize database items the right way, but how do we know what's what ? It is crucial to clearly define and differentiate between facts, attributes, and relationships to create an efficient and evolutive design . Here’s how you can identify each component and filter out unnecessary information. 

### Know the domain
It should make perfect sense that nobody ever created a decent data design on a domain it didn't know beforehand. To gaher that knowledge or learnt he missing bits : collect detailed requirements from stakeholders to understand what data needs to be stored and how it will be used. Without this intimate knowledge, it is impossible to filter out unnecessary information ( aka bullshit ). 

* What is a fact ?  
A fact is a fundamental element or entity that represents a real-world object or concept that you need to store information about. For exemaple customer, product, contract, home are facts. Facts are stored in tables with unique ids.

* What is an attribute ?   
An attribute is an intrinsic, usually immutable property or characteristic that provides more detail about a fact. Attributes describe the various facets of said afact. For exemplae, name, first name, colour, size are attributes. Attributes are stored in columns, each having its own.

* What is a relation ?  
A relation defines how two or more facts  interact with each other within the considered system. For exemplae : possessing, living in, purchasing, using are relations. Relations are stored in table containing the unique ids of the linked facts.

* _Rest is probably useless bulshit_   
Until it becomes usefull, but that's gonna be another discussion ( yeah i'll make a whole post about that. Later ).

  
Ain't it easy (peasy) ? Not that much indeed. Let's now have a look to a method that helps identifying the aforementionned 4 categories ( facts, attributes, relations and bullshit ).

### Use natural language
Natural language descriptions are invaluable in distinguishing attributes from facts and relationships.  
A fact is usually a noun that refers to a core concept of the domain we are modeling. Attributes provide specific details about the previous item (the fact), and natural language helps identify these details through descriptive terms and context. Relations are usually expressed by verbs linking facts between themselves.

Example  
  "Our e-commerce platform needs to manage customers, their orders, and the products they purchase. Customers have personal contact details such as name, first name and brithdate, and unique public ID. Each order includes an order date and can contain multiple products, each with a name and price."
      
* Facts: 
  - customer, order, product - materialized by different tables having unique ids
* Attributes:
  - Customer: unique public ID, name, first name, birthplace - materialized by one column per attribute in the corresponding table
  - Order: order date  - materialized by one colmun per attribute in the corresponding table
  - Product: name, price  - materialized by one colmun per attribute in the corresponding table
* Relationships:
  - A customer places orders - materliazed by a table linking the unique ids of each of the fact tables it does link.
  - An order contains products - materliazed by a table linking the unique ids of each of the fact tables it does link.

### Caveats
There are three main maistkae that can lead to wrong design. While it usually happens to attributes, some of those could alos lead to wrongly consider an item as a fact.

* Ambiguity   
Attributes may sometimes be ambiguously defined or interpreted, leading to confusion in their representation in the database schema.

* Overgeneralization  
It's crucial to avoid overgeneralizing attributes, as this can lead to capturing unnecessary or redundant information that doesn't add value to the database.

* Context Sensitivity  
Attributes often depend on the context in which they are used. The same term might have different meanings or requirements in different parts of the system.

Example  
The two most infamous caveats are phone number and address.  
The true wording about phone is : "My phone operatror granted me a line publicly identified by this phone number". The nmuber has an existence outisdethe person ( and also the device used to answer calls ) : those are different facts linked toghether by relations.  
The true wording about address is : " i live/possess in a home/building/plot of land that sits at this address." Address is a geogrpahical beacon that exists wether there is asomething or not, whomever possesses the palce sitting there. Address is a fact that is linked to a person by a relation.  
In both cases liking directly the fact to the user is a simplification but a necessary one.

### False friends
* Superficial Similarity  
Some terms may appear to be straightforward attributes but turn out to require deeper analysis due to their multifaceted nature or context-dependent usage.

* Misleading Names  
Certain terms might misleadingly suggest they are attributes when they are actually entities or relationships, requiring careful scrutiny during database schema design.

* Dynamic Data  
Some attributes might seem static but actually require dynamic calculation or updating, which affects their storage and retrieval in the database. Since they are not imutable they shoud never be considered as attributes.

Example  
The most infamous false friend is age. Despite being seemingly intrinsic age is not immutable. It is also not that intrinsic since all the people born the same day ahev the very sdame age. What should trigger your understanding is that age is a calculation that need knowing another attribute : birthdate and the day of calculation date. This is a dynamic attribute so it should not be stored nor even considereds at this stage of data design.

### Conclusion
Using natural language in this structured approach  ensures that you correctly identify the core entities (facts) in your database design, providing a solid foundation for further detailing and implementation. Beware to truly addressing the caveats and being aware of false friends. By strictly following thoise guidelines profesionnals in carge of data design can effectively identify and define attributes that accurately represent the data requirements of the system, fostering a robust and reliable database schema.

---

published in linkedin : 


---

Mentioned in [![Mentioned in Awesome MariaDB](https://awesome.re/mentioned-badge.svg)](https://github.com/Vettabase/awesome-mariadb)
