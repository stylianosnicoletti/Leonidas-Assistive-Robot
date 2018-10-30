package com.example.stelios.leoappjavamosquitto;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

public class LongGameGraphActivity extends AppCompatActivity {

    private String data = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_long_game_graph);

        GraphView graph = (GraphView) findViewById(R.id.graph);
        data = (String) getIntent().getSerializableExtra("data");

        String[] tokens = data.split(",\\s");

        DataPoint[] points = new DataPoint[tokens.length];

        for (int i=0; i<points.length; i++) {
            points[i] = new DataPoint(i, Double.parseDouble(tokens[i]));
        }

        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(points);
        graph.addSeries(series);
        graph.setTitle("Time taken for individual interactions");
        graph.getGridLabelRenderer().setHorizontalAxisTitle("Interaction number");
        graph.getGridLabelRenderer().setVerticalAxisTitle("Time taken");
    }
}
