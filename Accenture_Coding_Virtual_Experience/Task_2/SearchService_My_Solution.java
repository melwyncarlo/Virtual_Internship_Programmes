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
    public enum SearchType
    {
        ALL, 
        EQUALS_AND_IGNORE_CASE, 
        CONTAINS_AND_IGNORE_CASE 
    }

    private final ProductItemRepository productItemRepository;

    @Autowired
    public SearchService(ProductItemRepository productItemRepository)
    {
        this.productItemRepository = productItemRepository;
    }

    public List<ProductItem> searchForProductItems( String searchQuery, 
                                                    boolean searchNameColumn, 
                                                    boolean searchDescriptionColumn, 
                                                    SearchType searchType)
    {
        Iterable<ProductItem> selectItemsIterable = null;

        List<ProductItem> selectItemsList = new ArrayList<>();

        if (searchType == SearchType.ALL)
        {
            selectItemsIterable = this.productItemRepository.findAll();
        }
        else
        {
            if (searchNameColumn && searchDescriptionColumn)
            {
                if (searchType == SearchType.EQUALS_AND_IGNORE_CASE)
                {
                    selectItemsIterable = this.productItemRepository.findByNameIgnoreCaseEqualsOrDescriptionIgnoreCaseEquals(searchQuery, searchQuery);
                }
                else if (searchType == SearchType.CONTAINS_AND_IGNORE_CASE)
                {
                    selectItemsIterable = this.productItemRepository.findByNameIgnoreCaseContainingOrDescriptionIgnoreCaseContaining(searchQuery, searchQuery);
                }
            }
            else if (searchNameColumn)
            {
                if (searchType == SearchType.EQUALS_AND_IGNORE_CASE)
                {
                    selectItemsIterable = this.productItemRepository.findByNameIgnoreCaseEquals(searchQuery);
                }
                else if (searchType == SearchType.CONTAINS_AND_IGNORE_CASE)
                {
                    selectItemsIterable = this.productItemRepository.findByNameIgnoreCaseContaining(searchQuery);
                }
            }
            else if (searchDescriptionColumn)
            {
                if (searchType == SearchType.EQUALS_AND_IGNORE_CASE)
                {
                    selectItemsIterable = this.productItemRepository.findByDescriptionIgnoreCaseEquals(searchQuery);
                }
                else if (searchType == SearchType.CONTAINS_AND_IGNORE_CASE)
                {
                    selectItemsIterable = this.productItemRepository.findByDescriptionIgnoreCaseContaining(searchQuery);
                }
            }
        }

        selectItemsIterable.forEach(selectItemsList::add);

        return selectItemsList;
    }

    public List<Number> searchForProductIds( String searchQuery, 
                                             boolean searchNameColumn, 
                                             boolean searchDescriptionColumn, 
                                             SearchType searchType)
    {
        List<ProductItem> selectItemsList = searchForProductItems(searchQuery, searchNameColumn, searchDescriptionColumn, searchType);

        return selectItemsList.stream().map(ProductItem::getId).collect(Collectors.toList());
    }
}

