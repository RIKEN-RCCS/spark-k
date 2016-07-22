/* SimpleApp.java -*-Mode: Java; Coding: us-ascii;-*- */
/* Copyright The Apache Software Foundation. */
/* CODE TAKEN FROM http://spark.apache.org/docs/latest/quick-start.html */
import org.apache.spark.api.java.*;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.function.Function;

public class SimpleApp {
    public static void main(String[] args) {
	String logFile = "/opt/aics/spark/spark-1.6.2-bin-sparkk/README.md";
	SparkConf conf = new SparkConf().setAppName("Simple Application");
	JavaSparkContext sc = new JavaSparkContext(conf);
	JavaRDD<String> logData = sc.textFile(logFile).cache();

	long numAs = logData.filter(new Function<String, Boolean>() {
		public Boolean call(String s) { return s.contains("a"); }
	    }).count();

	long numBs = logData.filter(new Function<String, Boolean>() {
		public Boolean call(String s) { return s.contains("b"); }
	    }).count();

	System.out.println("Lines with a: " + numAs + ", lines with b: " + numBs);
    }
}
