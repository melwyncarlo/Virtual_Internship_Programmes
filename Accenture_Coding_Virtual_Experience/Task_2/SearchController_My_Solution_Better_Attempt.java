package com.mockcompany.webapp.controller;

import java.util.Collection;
import com.mockcompany.webapp.model.ProductItem;
import com.mockcompany.webapp.service.SearchService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SearchController
{
    private final SearchService searchService;

    @Autowired
    public SearchController(SearchService searchService)
    {
        this.searchService = searchService;
    }

    @GetMapping("/api/products/search")
    public Collection<ProductItem> search(@RequestParam("query") String query)
    {
        return this.searchService.searchForProductItems(query);
    }
}

