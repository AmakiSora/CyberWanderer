package dao;

import FakerData.pojo.Person;
import FakerData.pojo.Product;

import java.util.List;

public interface FakerDataDao {
    void insertPerson(Person person);
    void insertPersons(List<Person> l);
    void insertProduct(List<Product> l);
}
