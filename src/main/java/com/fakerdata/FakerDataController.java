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
    //http://localhost:4567/getProduct
    @GetMapping("/getProduct")
    public String getProduct() throws Exception {
        return getProduct.get(600);
    }
    //http://localhost:4567/getPersons
    @GetMapping("/getPersons")
    public String getPersons() throws Exception {
        return getPersons.get(600);
    }
}
