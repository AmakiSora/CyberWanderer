package com.fakerdata;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class FakerDataController {
    @Autowired
    private GetProduct getProduct;
    @Autowired
    private GetPersons getPersons;
    @GetMapping("/getProduct")
    public String getProduct() throws Exception {
        return getProduct.get(10);
    }
    @GetMapping("/getPersons")
    public String getPersons() throws Exception {
        return getPersons.get(10);
    }
}
