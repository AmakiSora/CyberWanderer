package dao;

import FakerData.pojo.Person;

import java.util.List;

public interface FakerDataDao {
    void insertPerson(Person person);
    void insertPersons(List<Person> lp);
}
