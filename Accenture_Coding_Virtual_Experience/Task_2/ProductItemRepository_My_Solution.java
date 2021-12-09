package com.mockcompany.webapp.data;

import com.mockcompany.webapp.model.ProductItem;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

/**
 * This Spring pattern is Java/Spring magic.  At runtime, spring will generate an implementation of this class based on
 * the name/arguments of the method signatures defined in the interface.  See this link for details on doing data access:
 *
 * https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#jpa.query-methods
 *
 * It's also possible to do specific queries using the @Query annotation:
 *
 * https://www.baeldung.com/spring-data-jpa-query
 */
@Repository
public interface ProductItemRepository extends CrudRepository<ProductItem, Long>
{
    Iterable<ProductItem> findByNameIgnoreCaseEquals(String inputQuery);
    Iterable<ProductItem> findByNameIgnoreCaseContaining(String inputQuery);

    Iterable<ProductItem> findByDescriptionIgnoreCaseEquals(String inputQuery);
    Iterable<ProductItem> findByDescriptionIgnoreCaseContaining(String inputQuery);

    Iterable<ProductItem> findByNameIgnoreCaseEqualsOrDescriptionIgnoreCaseEquals(String inputQuery1, String inputQuery2);
    Iterable<ProductItem> findByNameIgnoreCaseContainingOrDescriptionIgnoreCaseContaining(String inputQuery1, String inputQuery2);
}

