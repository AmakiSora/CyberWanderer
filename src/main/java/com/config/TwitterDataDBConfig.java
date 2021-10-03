package com.config;

import org.apache.ibatis.session.SqlSessionFactory;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.SqlSessionTemplate;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

import javax.sql.DataSource;

@Configuration
@MapperScan(basePackages = "com.twitter.twitterDataDao",sqlSessionFactoryRef = "twitterdatadbSqlSessionFactory")
public class TwitterDataDBConfig {
    @Value("${spring.twitterdatadb.datasource.driver-class-name}")
    String driverClass;
    @Value("${spring.twitterdatadb.datasource.url}")
    String url;
    @Value("${spring.twitterdatadb.datasource.username}")
    String userName;
    @Value("${spring.twitterdatadb.datasource.password}")
    String passWord;
    @Bean(name = "twitterdatadbDataSource")
    @ConfigurationProperties("spring.twitterdatadb.datasource")
    public DataSource twitterdatadbDataSource() {
        DriverManagerDataSource dataSource = new DriverManagerDataSource();
        dataSource.setDriverClassName(driverClass);
        dataSource.setUrl(url);
        dataSource.setUsername(userName);
        dataSource.setPassword(passWord);
        return dataSource;
    }
    @Bean(name = "twitterdatadbSqlSessionFactory")
    @Primary
    public SqlSessionFactory twitterdatadbSqlSessionFactory(@Qualifier("twitterdatadbDataSource") DataSource dataSource) throws Exception {
        SqlSessionFactoryBean sessionFactoryBean = new SqlSessionFactoryBean();
        sessionFactoryBean.setDataSource(dataSource);
        sessionFactoryBean.setMapperLocations(new PathMatchingResourcePatternResolver()
                .getResources("classpath*:mapper/twitterdataMapper/*.xml"));//第一个mapper.xml
        //配置多数据源需要设置驼峰规则，否则不生效
        org.apache.ibatis.session.Configuration configuration=new org.apache.ibatis.session.Configuration();
        configuration.setMapUnderscoreToCamelCase(true);
        sessionFactoryBean.setConfiguration(configuration);
        return sessionFactoryBean.getObject();
    }
    @Bean(name = "twitterdatadbSqlSessionTemplate")
    public SqlSessionTemplate sqlSessionFactoryTemplate(@Qualifier("twitterdatadbSqlSessionFactory") SqlSessionFactory sqlSessionFactory) throws Exception {
        return new SqlSessionTemplate(sqlSessionFactory);
    }
}
