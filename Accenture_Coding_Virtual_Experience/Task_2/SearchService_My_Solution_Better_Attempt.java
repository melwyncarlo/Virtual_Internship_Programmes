package com.mockcompany.webapp.service;

import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import com.mockcompany.webapp.model.ProductItem;
import com.mockcompany.webapp.data.ProductItemRepository;
import org.springframework.beans.factory.annotation.Autowired;

@Service
public class SearchService
{
    private final ProductItemRepository productItemRepository;

    @Autowired
    public SearchService(ProductItemRepository productItemRepository)
    {
        this.productItemRepository = productItemRepository;
    }

    public List<ProductItem> searchForProductItems(String searchQuery)
    {
        List<ProductItem> selectItemsList = new ArrayList<>();

        Iterable<ProductItem> selectItemsIterable = null;

        searchQuery = searchQuery.trim();

        if (searchQuery.length() == 0)
        {
            selectItemsIterable = this.productItemRepository.findAll();
        }
        else if ((searchQuery.startsWith("\"") && searchQuery.endsWith("\"")) 
        ||       (searchQuery.startsWith("\'") && searchQuery.endsWith("\'")))
        {
            searchQuery = searchQuery.substring(1, searchQuery.length() - 1);

            selectItemsIterable = this.productItemRepository.findByNameIgnoreCaseEqualsOrDescriptionIgnoreCaseEquals(searchQuery, searchQuery);
        }
        else
        {
            selectItemsIterable = this.productItemRepository.findByNameIgnoreCaseContainingOrDescriptionIgnoreCaseContaining(searchQuery, searchQuery);
        }

        selectItemsIterable.forEach(selectItemsList::add);

        return selectItemsList;
    }

    public List<Number> searchForProductIds(String searchQuery)
    {
        List<ProductItem> selectItemsList = searchForProductItems(searchQuery);

        return selectItemsList.stream().map(ProductItem::getId).collect(Collectors.toList());
    }
}

