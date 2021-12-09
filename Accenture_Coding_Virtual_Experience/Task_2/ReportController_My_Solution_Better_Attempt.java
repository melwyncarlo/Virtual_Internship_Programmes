package com.mockcompany.webapp.controller;

import java.util.HashMap;
import com.mockcompany.webapp.service.SearchService;
import com.mockcompany.webapp.api.SearchReportResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ReportController
{
    private static final String searchKeyWordsList[] = { "Cool", "Kids", "Amazing", "Perfect" };

    private final SearchService searchService;

    @Autowired
    public ReportController(SearchService searchService)
    {
        this.searchService = searchService;
    }

    @GetMapping("/api/products/report")
    public SearchReportResponse runReport()
    {
        SearchReportResponse response = new SearchReportResponse();
        response.setSearchTermHits(new HashMap<>());

        /* Get the total number of products count. */
        response.setProductCount(this.searchService.searchForProductItems("").size());

        for (String searchKeyWord : searchKeyWordsList)
        {
            response.getSearchTermHits().put(searchKeyWord, this.searchService.searchForProductIds(searchKeyWord).size());
        }

        return response;
    }
}

