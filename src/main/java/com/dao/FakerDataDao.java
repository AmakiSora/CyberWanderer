package com.dao;

import com.fakerdata.pojo.Person;
import com.fakerdata.pojo.Product;
import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import java.util.List;
@Mapper
@Repository
public interface FakerDataDao {
    void insertPerson(Person person);
    void insertPersons(List<Person> l);
    void insertProduct(List<Product> l);
}
