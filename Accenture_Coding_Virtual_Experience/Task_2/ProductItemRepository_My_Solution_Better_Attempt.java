package com.mockcompany.webapp.data;

import com.mockcompany.webapp.model.ProductItem;
import org.springframework.stereotype.Repository;
import org.springframework.data.repository.CrudRepository;

@Repository
public interface ProductItemRepository extends CrudRepository<ProductItem, Long>
{
    Iterable<ProductItem> findByNameIgnoreCaseEqualsOrDescriptionIgnoreCaseEquals(String inputQuery1, String inputQuery2);
    Iterable<ProductItem> findByNameIgnoreCaseContainingOrDescriptionIgnoreCaseContaining(String inputQuery1, String inputQuery2);
}

