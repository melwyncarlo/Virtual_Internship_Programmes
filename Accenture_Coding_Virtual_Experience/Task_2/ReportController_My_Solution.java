package com.mockcompany.webapp.controller;

import java.util.Map;
import java.util.List;
import java.util.HashMap;
import com.mockcompany.webapp.model.ProductItem;
import com.mockcompany.webapp.service.SearchService;
import com.mockcompany.webapp.api.SearchReportResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;

/**
 * Management decided it is super important that we have lots of products that match the following terms.
 * So much so, that they would like a daily report of the number of products for each term along with the total
 * product count.
 */
@RestController
public class ReportController
{
    /**
     * The people that wrote this code didn't know about JPA Spring Repository interfaces!
     */
    private final SearchService searchService;

    @Autowired
    public ReportController(SearchService searchService)
    {
        this.searchService = searchService;
    }

    @GetMapping("/api/products/report")
    public SearchReportResponse runReport()
    {
        Map<String, Integer> hits = new HashMap<>();
        SearchReportResponse response = new SearchReportResponse();
        response.setSearchTermHits(hits);

        List<ProductItem> allItems = this.searchService.searchForProductItems("", false, false, SearchService.SearchType.ALL);

        int count = allItems.size();

        List<Number> resultantIds = this.searchService.searchForProductIds("cool", true, true, SearchService.SearchType.CONTAINS_AND_IGNORE_CASE);

        response.getSearchTermHits().put("Cool", resultantIds.size());

        response.setProductCount(count);

        response.getSearchTermHits().put("Kids", this.searchService.searchForProductItems("kids", true, true, SearchService.SearchType.CONTAINS_AND_IGNORE_CASE).size());

        response.getSearchTermHits().put("Amazing", this.searchService.searchForProductItems("amazing", true, true, SearchService.SearchType.CONTAINS_AND_IGNORE_CASE).size());

        hits.put("Perfect", this.searchService.searchForProductItems("perfect", true, true, SearchService.SearchType.CONTAINS_AND_IGNORE_CASE).size());

        return response;
    }
}

