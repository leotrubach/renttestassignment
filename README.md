# Requirements / Tasks

1. Please change the models so that the following functionality works. How do you test it?
    I need to mention that it is better to have this business logic on view level,
    but since it is required to do on models level, here is the solution

    - **A Company can have one or more offices**
    
        This could be achieved by adding `company` `ForeignKey` field to `Office` model
    
    - **Offices can be an headquarter.**
    
        I was thinking about it and I see 2 ways of implementing it:
        * add a `is_headquarters` `BooleanField` to `Office` model
        * add `headquarters` OneToOne field to `Company` model
        The latter approach looks better to me, since it allows us to ensure on database level 
        that:
        - no office can be headquarters for 2 companies (due to fact that OneToOne 
          field implies uniqueness)
        - company will not have more than one headquarter  
        
    - **A company should at all times have exactly one headquarter**
        I'm not sure that it is possible to do this at `models.py` level for cases
        when Company has just been created. But once we have assigned headquarters,
        we can do it.
        First of all it is done by setting `on_delete` kwarg for Company.headquarters
        to `models.PROTECT` ensuring that Company will not lose its headquarters if 
        someone wishes to delete `Office` instance that is headquarter
        Second, we can disallow setting `headquarters` to `None` once it has been
        assigned
        Third, we can disallow to change `company` field of `Office` instance if the
        office is `headquarters` of that company    
    
    I have prepared unit test case named `CompanyTest` 

2. Please add an API with the help of django-rest-framework. How would you test the functionality?

    - Write an simple read-only API endpoint for companies to get the company name + street+postal_code+city from the headquarter office
    - Write an simple read-only API endpoint to get all the offices for a company
        Implemented it in CompanyListViewSet.offices()
    
    - Write an API endpoint to change the headquarter of the company
        Implemented Custom serializer with `get_fields()` methods that adjusts
        `queryset` for `headquarters` limiting it to company offices prior to validation.

3. BONUS: 

    - **Customize the API endpoint to include the sum of rent for all offices of a Company. How would you approach / test this?**
       Added `.annotate(total_rent=Sum('office__monthly_rent'))` to queryset in company list view
       Wrote test `test_monthly_rent` that creates 10 companies, for every company creates 10 offices with random
       price for monthly rent. After that checked that totals in response are equal to totals of randomly
       generated numbers.  