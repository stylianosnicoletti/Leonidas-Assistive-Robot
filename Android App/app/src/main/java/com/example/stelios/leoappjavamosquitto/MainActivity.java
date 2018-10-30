package com.example.stelios.leoappjavamosquitto;

import android.net.Uri;
import android.support.v4.view.PagerAdapter;
import android.support.v4.view.ViewPager;
import android.bluetooth.BluetoothServerSocket;
import android.content.Context;
import android.content.Intent;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.NavigationView;
import android.support.design.widget.Snackbar;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import com.afollestad.materialdialogs.DialogAction;
import com.afollestad.materialdialogs.MaterialDialog;
import com.parse.Parse;
import com.parse.ParseException;
import com.parse.ParseObject;
import com.parse.ParseQuery;
import com.parse.ParseInstallation;
import com.parse.SaveCallback;

public class MainActivity extends AppCompatActivity implements org.eclipse.paho.client.mqttv3.MqttCallback, NavigationView.OnNavigationItemSelectedListener {

    //    private OutputStream outputStream;
    private InputStream inStream;
    private BluetoothServerSocket mmServerSocket;
    private MqttClient client;
    private MqttMessage msg0;
    private MqttMessage msg1;
    private MqttMessage msg2;
    private MqttMessage msg3;
    private MqttMessage msg4;
    private MqttMessage msg5;
    private MqttMessage msg6;
    private MqttMessage msg7;
    private MqttMessage msg8;
    private MqttMessage msg9;
    private MqttMessage msg10;
    private MqttMessage msg11;
    private MqttMessage msg12;
    private MqttMessage msg13;
    private MqttMessage msg14;
    private MqttMessage msg15;
    private MqttMessage msg16;
    private MqttMessage msg17;
    private MqttMessage msgCancel;
    private ArrayList<Double> listTimes;
    private ArrayList<Double> times;
    private ArrayList<Integer> listScores;
    private ArrayList<Integer> scores;
    private List<ParseObject> objTimes;
    private List<ParseObject> objScores;
    private StringBuilder sb;
    private FloatingActionButton fab;
    private MqttConnectOptions timeOut;
    private String email;
    private EditText em;
    private TextView user, sc;
    private int netScore;
    private boolean flag;

    // viewpager code
    private View view1, view2, view3, view4, view5, view6;
    private ViewPager viewPager;
    private List<View> viewList;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_side);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        listScores = new ArrayList<>();
        listTimes = new ArrayList<>();
        times = new ArrayList<>();
        scores = new ArrayList<>();
        netScore = 0;
        sb = new StringBuilder();
        Parse.initialize(this);
        ParseInstallation.getCurrentInstallation().saveInBackground();
        //setSupportActionBar(toolbar)


        email = (String)getIntent().getSerializableExtra("email");


        // Viewpager code
        viewPager = (ViewPager) findViewById(R.id.viewpager);
        LayoutInflater inflater=getLayoutInflater();
        view1 = inflater.inflate(R.layout.content_main_activity_side, null);
        view2 = inflater.inflate(R.layout.memory_game_layout,null);
        view3 = inflater.inflate(R.layout.reaction_game_layout,null);
        view4 = inflater.inflate(R.layout.face_detection_layout,null);
        view5 = inflater.inflate(R.layout.data_analysis, null);
        view6 = inflater.inflate(R.layout.settings, null);
        em = (EditText) view6.findViewById(R.id.em);
        user = (TextView) view6.findViewById(R.id.user);
        sc = (TextView) view6.findViewById(R.id.sco);

        em.setText("Email: " + email);
        user.setText("Username: " + email.substring(0, email.indexOf("@")));


        viewList = new ArrayList<View>();
        viewList.add(view1);
        viewList.add(view2);
        viewList.add(view3);
        viewList.add(view4);
        viewList.add(view5);
        viewList.add(view6);


        PagerAdapter pagerAdapter = new PagerAdapter() {
            @Override
            public boolean isViewFromObject(View arg0, Object arg1) {
                // TODO Auto-generated method stub
                return arg0 == arg1;
            }

            @Override
            public int getCount() {
                // TODO Auto-generated method stub
                return viewList.size();
            }

            @Override
            public void destroyItem(ViewGroup container, int position,
                                    Object object) {
                // TODO Auto-generated method stub
                container.removeView(viewList.get(position));
            }

            @Override
            public Object instantiateItem(ViewGroup container, int position) {
                // TODO Auto-generated method stub
                container.addView(viewList.get(position));


                return viewList.get(position);
            }
        };

        viewPager.setAdapter(pagerAdapter);


        // end of viewpager


        fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(handleClick);

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);



        final MaterialDialog.Builder dialogBuilder = new MaterialDialog.Builder(this)
                .title(R.string.title)
                .content(R.string.content)
                .positiveText(R.string.agree)
                .negativeText(R.string.disagree)
                .onPositive(new MaterialDialog.SingleButtonCallback() {
                    @Override
                    public void onClick(MaterialDialog dialog, DialogAction which) {
                        createConnection();


                    }
                })
                .onNegative(new MaterialDialog.SingleButtonCallback() {
                    @Override
                    public void onClick(MaterialDialog dialog, DialogAction which) {
                        finish();
                    }
                });

        final MaterialDialog connectionDialog = dialogBuilder.build();
        connectionDialog.show();

    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main_activity_side, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.nav_basic_game) {
            // Handle the camera action
            viewPager.setCurrentItem(0,true);

        } else if (id == R.id.nav_memory_game) {
            viewPager.setCurrentItem(1,true);

        } else if (id == R.id.nav_reaction_game) {
            viewPager.setCurrentItem(2,true);

        } else if (id == R.id.nav_detect_face) {
            viewPager.setCurrentItem(3,true);

        } else if (id == R.id.nav_data_analysis) {
            viewPager.setCurrentItem(4, true);
        }
        else if (id == R.id.action_settings) {
            viewPager.setCurrentItem(5, true);

            //Creating settings activity
            int userScore = 0;
            double userTime = 0;

            if (listTimes.size() !=0) {
                for (double time : listTimes) {
                    userTime = userTime + time;
                }
                userTime = userTime / listTimes.size();
            }

            if (listScores.size() !=0) {
                for (int score : listScores) {
                    userScore = userScore + score;
                }
                userScore = userScore / listScores.size();
            }

            int finalScore = 0;

            if(userTime != 0 && userScore !=0) {
                finalScore = (int) Math.round(userScore/userTime);
            }

            Log.d("What", String.valueOf(finalScore));
            sc.setText("Score: " + finalScore);
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    private View.OnClickListener handleClick = new View.OnClickListener() {
        @Override
        public void onClick(View view) {

            sb = new StringBuilder();
            sb.append("Reaction Times: \t");

            if (listTimes != null) {
                for (Double s : listTimes) {
                    sb.append(s.toString() + "s" + "\t");
                }
            }

            sb.append("\n");

            sb.append("Scores: \t");

            if (listScores != null) {
                for (Integer s : listScores) {
                    sb.append(s.toString() + " " + "points" + "\t");
                }
            }

            sb.append("\n");

            if (em.getText() != null) {
                email = em.getText().toString();
            }
            Log.d("WHATT", email);
            Intent emailIntent = new Intent(Intent.ACTION_SENDTO);
            emailIntent.setData(Uri.parse("mailto:" + email));
            emailIntent.putExtra(Intent.EXTRA_SUBJECT, "User data for" + " " + email.substring(0, email.indexOf("@")));
            emailIntent.putExtra(Intent.EXTRA_TEXT, "Please find the data in this email for the client \n" + sb.toString());

            try {
                startActivity(Intent.createChooser(emailIntent, "Send email with"));
                Snackbar.make(view, "Sent patient information", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            } catch (android.content.ActivityNotFoundException ex) {
                Toast.makeText(MainActivity.this, "Email is nto verified!", Toast.LENGTH_SHORT).show();
            }
        }
    };

    public void createConnection() {

        // Setting timeout Interval for connection
        timeOut = new MqttConnectOptions();
        timeOut.setKeepAliveInterval(60000);
        Log.d("Main", "Trying!");

        try {
            //"tcp://10.42.0.1:1883"
            client = new MqttClient("tcp://10.42.0.1:1883", "AndroidThingSub", new MemoryPersistence());
            client.setCallback(this);

            // Connect client with Mqqt option timeOut initialised above
            client.connect(timeOut);

            // Reaction Game 1 Demo
            String stringMsg0 = new String ("0");
            byte[] b0 = stringMsg0.getBytes();
            msg0 = new MqttMessage(b0);

            // Say Hello
            String stringMsg1 = new String ("1");
            byte[] b1 = stringMsg1.getBytes();
            msg1 = new MqttMessage(b1);

            // Reaction Game 2
            String stringMsg2 = new String ("2");
            byte[] b2 = stringMsg2.getBytes();
            msg2 = new MqttMessage(b2);

            // Reaction Game 3
            String stringMsg3 = new String ("3");
            byte[] b3 = stringMsg3.getBytes();
            msg3 = new MqttMessage(b3);

            // Reaction Game 4
            String stringMsg4 = new String ("4");
            byte[] b4 = stringMsg4.getBytes();
            msg4 = new MqttMessage(b4);

            // Reaction Game 5
            String stringMsg5 = new String ("5");
            byte[] b5 = stringMsg5.getBytes();
            msg5 = new MqttMessage(b5);

            // Start Detect
            String stringMsg6 = new String ("6");
            byte[] b6 = stringMsg6.getBytes();
            msg6 = new MqttMessage(b6);

            // Memory Game Prestige
            String stringMsg7 = new String ("7");
            byte[] b7 = stringMsg7.getBytes();
            msg7 = new MqttMessage(b7);

            // Memory Game Very Easy
            String stringMsg8 = new String ("8");
            byte[] b8 = stringMsg8.getBytes();
            msg8 = new MqttMessage(b8);

            // Memory Game Easy
            String stringMsg9 = new String ("9");
            byte[] b9 = stringMsg9.getBytes();
            msg9 = new MqttMessage(b9);

            // Memory Game Normal
            String stringMsg10 = new String ("10");
            byte[] b10 = stringMsg10.getBytes();
            msg10 = new MqttMessage(b10);

            // Memory Game Hard
            String stringMsg11 = new String ("11");
            byte[] b11 = stringMsg11.getBytes();
            msg11 = new MqttMessage(b11);

            // Memory Game Very Hard
            String stringMsg12 = new String ("12");
            byte[] b12 = stringMsg12.getBytes();
            msg12 = new MqttMessage(b12);

            // Wiggle Hand
            String stringMsg13 = new String ("13");
            byte[] b13 = stringMsg13.getBytes();
            msg13 = new MqttMessage(b13);

            // Move Forward
            String stringMsg14 = new String ("14");
            byte[] b14 = stringMsg14.getBytes();
            msg14 = new MqttMessage(b14);

            // Move Backward
            String stringMsg15 = new String ("15");
            byte[] b15 = stringMsg15.getBytes();
            msg15 = new MqttMessage(b15);

            // Turn Around
            String stringMsg16 = new String ("16");
            byte[] b16 = stringMsg16.getBytes();
            msg16 = new MqttMessage(b16);

            // Move Forward
            String stringMsg17 = new String ("17");
            byte[] b17 = stringMsg17.getBytes();
            msg17 = new MqttMessage(b17);


            String stringMsgc = new String ("-1");
            byte[] bc = stringMsgc.getBytes();
            msgCancel = new MqttMessage(bc);

            client.subscribe("topic/android/dt");

            Context context = getApplicationContext();
            CharSequence text = "Connected!";
            int duration = Toast.LENGTH_SHORT;
            Toast.makeText(context, text, duration).show();

        } catch (MqttException e) {
            e.printStackTrace();
            Context context = getApplicationContext();
            CharSequence text = "Did not connect!";
            int duration = Toast.LENGTH_SHORT;
            Toast.makeText(context, text, duration).show();
            Log.d("Main", "Can't!");
        }

    }

    public void Reaction1(View view) {
        try {
            client.publish("topic/rpi/dt",msg0);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void SayHello(View view) {
        try {
            client.publish("topic/rpi/dt",msg1);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void Reaction2(View view) {
        try {
            client.publish("topic/rpi/dt",msg2);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void Reaction3(View view) {
        try {
            client.publish("topic/rpi/dt",msg3);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void Reaction4(View view) {
        try {
            client.publish("topic/rpi/dt",msg4);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void Reaction5(View view) {
        try {
            client.publish("topic/rpi/dt",msg5);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void FaceDetect(View view) {
        try {
            client.publish("topic/rpi/dt",msg6);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void MemoryPrestige(View view) {
        try {
            client.publish("topic/rpi/dt",msg7);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void MemoryVeryEasy(View view) {
        try {
            client.publish("topic/rpi/dt",msg8);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void MemoryEasy(View view) {
        try {
            client.publish("topic/rpi/dt",msg9);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void MemoryNormal(View view) {
        try {
            client.publish("topic/rpi/dt",msg10);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void MemoryHard(View view) {
        try {
            client.publish("topic/rpi/dt",msg11);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void MemoryVeryHard(View view) {
        try {
            client.publish("topic/rpi/dt",msg12);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void WiggleHand(View view) {
        try {
            client.publish("topic/rpi/dt",msg13);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void MoveForward(View view) {
        try {
            client.publish("topic/rpi/dt",msg14);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void MoveBackward(View view) {
        try {
            client.publish("topic/rpi/dt",msg15);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void TurnAround(View view) {
        try {
            client.publish("topic/rpi/dt",msg16);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void Spin(View view) {
        try {
            client.publish("topic/rpi/dt",msg17);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void StopGame(View view) {
        try {
            client.publish("topic/rpi/dt",msgCancel);
        } catch (MqttPersistenceException e) {
            e.printStackTrace();
        } catch (MqttException e) {
            e.printStackTrace();
        }

        Context context = getApplicationContext();
        CharSequence text = "Connection terminated!";
        int duration = Toast.LENGTH_SHORT;
        Toast.makeText(context, text, duration).show();

    }

    public void SeeResult(View view) {
        /*Intent intent= new Intent(MainActivity.this,ResultsActivity.class);
        intent.putExtra("data", (ArrayList<String>) lista);
        startActivity(intent);*/

    }

    public void AnalyseData(View view) {

        try {
            ParseQuery queryData = ParseQuery.getQuery("LeoData");
            queryData.whereExists("data");
            objTimes = queryData.find();
        } catch (com.parse.ParseException e) {
            e.printStackTrace();
        }
        try {
            ParseQuery queryScore = ParseQuery.getQuery("LeoData");
            queryScore.whereExists("score");
            objScores = queryScore.find();
        } catch (com.parse.ParseException e) {
            e.printStackTrace();
        }


        int netScore = 0;
        double netTime = 0;

        for (ParseObject obj : objTimes) {
            times.add(Double.parseDouble(obj.getString("data")));
            //Log.d("Data", obj.getString("data"));
        }
        for (ParseObject obj: objScores) {
            String sc = obj.getString( "score");
            sc = sc.replaceAll("\\s", "");
            //Log.d("score", sc);
            scores.add(Integer.parseInt(sc));
        }

        for (double time: times){
            netTime = netTime + time;
        }
        netTime = netTime/times.size();

        for (int score: scores){
            netScore = netScore + score;
        }
        netScore = netScore/scores.size();



        int userScore = 0;
        double userTime = 0;

        if (listTimes.size() !=0) {
            for (double time : listTimes) {
                userTime = userTime + time;
            }
            userTime = userTime / listTimes.size();
        }

        if (listScores.size() !=0) {
            for (int score : listScores) {
                userScore = userScore + score;
            }
            userScore = userScore / listScores.size();
        }

        Log.d("NET TIME", String.valueOf(netTime));
        Log.d("NET SCORE", String.valueOf(netScore));

        Log.d("USER TIME", String.valueOf(userTime));
        Log.d("USER SCORE", String.valueOf(userScore));

        final TextView display = findViewById(R.id.textView11);
        final TextView display2 = findViewById(R.id.textView10);

        if (userTime<=netTime) {
            display.setText("Please choose a harder reaction game!");
        }
        else {
            display.setText("Please pick an easier reaction game!");
        }

        if (userScore>netScore) {
            display2.setText("Please choose a harder memory game!");
        }
        else {
            display2.setText("Please pick an easier memory game!");
        }

    }

    @Override
    public void connectionLost(Throwable cause) {

        Context context = getApplicationContext();
        CharSequence text = "Connection Lost!";
        int duration = Toast.LENGTH_SHORT;
        Toast.makeText(context, text, duration).show();

//        flag = false;

    }

    @Override
    public void messageArrived(String topic, MqttMessage message) throws Exception {

        String a = message.toString();
        a = a.substring(2);
        a = a.replaceAll("[\"\'\\[\\]]","");


        if (a.substring(0, 1).equals("S")) {
            String b = a.substring(a.indexOf(" "));
            b = b.trim();
            listScores.add(Integer.parseInt(b));
            ParseObject parseObject = new ParseObject("LeoData");
            parseObject.put("score", b);
            parseObject.saveInBackground(new SaveCallback() {
                @Override
                public void done(ParseException e) {
                    Context context = getApplicationContext();
                    CharSequence text = "Saved on server successfully!";
                    int duration = Toast.LENGTH_LONG;
                    if (e == null)
                        Toast.makeText(context, text, duration).show();
                    else

                        Toast.makeText(context, e.getMessage(), duration).show();
                }
            });
        }

        else if (a.substring(0, 1).equals("R")) {
            Log.d("Robot", a);
        }

        else if (a.length() < 6) {
            listTimes.add(Double.parseDouble(a));
            ParseObject parseObject = new ParseObject("LeoData");
            parseObject.put("data", a);
            parseObject.saveInBackground(new SaveCallback() {
                @Override
                public void done(ParseException e) {
                    Context context = getApplicationContext();
                    CharSequence text = "Saved on server successfully!";
                    int duration = Toast.LENGTH_SHORT;
                    if (e == null)
                        Toast.makeText(context, text, duration).show();
                    else
                        Toast.makeText(context, e.getMessage(), duration).show();
                }
            });
        }

        else {
            String[] tokens = a.split(",\\s");
            for (String obj:tokens) {
                listTimes.add(Double.parseDouble(obj));
                ParseObject parseObj = new ParseObject("LeoData");
                parseObj.put("data", obj);
                parseObj.saveInBackground(new SaveCallback() {
                    @Override
                    public void done(ParseException e) {
                        Context context = getApplicationContext();
                        CharSequence text = "Saved on server successfully!";
                        int duration = Toast.LENGTH_LONG;
                        if (e == null)
                            Toast.makeText(context, text, duration).show();
                        else
                            Toast.makeText(context, e.getMessage(), duration).show();
                    }
                });
            }
        }


        //Memory game or Robot says hello or Move Hands
        if (a.substring(0, 1).equals("S") || a.substring(0, 1).equals("R") || a.length() < 6) {
            Intent intent = new Intent(MainActivity.this, ResultsActivity.class);
            intent.putExtra("data", a);
            startActivity(intent);
        }
        //Long game
        else {
            Intent intent = new Intent(MainActivity.this, LongGameGraphActivity.class);
            intent.putExtra("data", a);
            startActivity(intent);
        }

        System.out.println(a);
        System.out.println("**************************");
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken token) {

    }
}
