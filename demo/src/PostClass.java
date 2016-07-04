import java.awt.Point;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.swing.JOptionPane;

import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import org.jnativehook.keyboard.NativeKeyEvent;
import org.jnativehook.keyboard.NativeKeyListener;
import org.jnativehook.mouse.NativeMouseEvent;
import org.jnativehook.mouse.NativeMouseMotionListener;

import argo.jdom.JsonNode;
import argo.jdom.JsonNodeFactories;
import argo.jdom.JsonRootNode;
import argo.jdom.JsonStringNode;


public class PostClass {

	private static boolean enabled;
	private static int DURATION = 1000;

	public static void main(String[] args) throws InterruptedException, NativeHookException, IOException {
		if (args.length > 0) {
			DURATION = Integer.parseInt(args[0]);
			System.out.println("Applied duration = " + DURATION);
			if (DURATION < 100) {
				System.out.println("Duration to small");
				return;
			}
		}

		final Queue<Point> ps = new ConcurrentLinkedQueue<>();

		// Get the logger for "org.jnativehook" and set the level to off.
		Logger logger = Logger.getLogger(GlobalScreen.class.getPackage().getName());
		logger.setLevel(Level.OFF);

		// Change the level for all handlers attached to the default logger.
		Handler[] handlers = Logger.getLogger("").getHandlers();
		for (int i = 0; i < handlers.length; i++) {
			handlers[i].setLevel(Level.OFF);
		}

		GlobalScreen.registerNativeHook();

		GlobalScreen.addNativeKeyListener(new NativeKeyListener() {

			@Override
			public void nativeKeyTyped(NativeKeyEvent arg0) {
			}

			@Override
			public void nativeKeyReleased(NativeKeyEvent arg0) {
				if (arg0.getKeyCode() == NativeKeyEvent.VC_CONTROL_L) {
					enabled = false;
					try {
						doIt(ps);
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			}

			@Override
			public void nativeKeyPressed(NativeKeyEvent arg0) {
				if (enabled) {
					return;
				}

				if (arg0.getKeyCode() == NativeKeyEvent.VC_CONTROL_L) {
					enabled = true;
				}
			}
		});

		GlobalScreen.addNativeMouseMotionListener(new NativeMouseMotionListener() {

			@Override
			public void nativeMouseMoved(NativeMouseEvent arg0) {
				if (enabled) {
					ps.add(new Point(arg0.getX(), arg0.getY()));
				}
			}

			@Override
			public void nativeMouseDragged(NativeMouseEvent arg0) {
			}
		});

		Thread.sleep(20000);
		GlobalScreen.unregisterNativeHook();
	}

	private static void doIt(final Queue<Point> ps) throws IOException {
		List<JsonNode> points = new ArrayList<>(ps.size());

		final int size = ps.size();
		System.out.println(size);

		for (int i = 0 ;i < size; i++) {
			Point p = ps.poll();
			JsonNode comer = pointToNode(p);
			points.add(comer);
		}

		post(JsonNodeFactories.object(
				JsonNodeFactories.field(
					"data", JsonNodeFactories.array(points))));
	}

	private static JsonNode pointToNode(Point p) {
		return JsonNodeFactories.array(
				JsonNodeFactories.number(p.x),
				JsonNodeFactories.number(p.y));
	}

	private static void post(JsonNode content) throws IOException {
		byte[] out = JSONUtility.jsonToString(content.getRootNode()).getBytes(Charset.forName("UTF-8"));
		int length = out.length;

		URL url = new URL("http://localhost:8000");
		URLConnection con = url.openConnection();
		HttpURLConnection http = (HttpURLConnection)con;
		http.setRequestMethod("POST"); // PUT is another valid option
		http.setDoOutput(true);
		http.setFixedLengthStreamingMode(length);
		http.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
		http.connect();
		try (OutputStream os = http.getOutputStream()) {
		    os.write(out);
		    os.flush();
		}

		int responseCode = http.getResponseCode();
//		System.out.println("\nSending 'POST' request to URL : " + url);
//		System.out.println("Response Code : " + responseCode);

		String result = null;
		try (BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()))) {
			String inputLine;
			StringBuilder response = new StringBuilder();

			while ((inputLine = in.readLine()) != null) {
				response.append(inputLine);
			}

			// print result
			result = response.toString();
		}

		JsonRootNode parsed = JSONUtility.jsonFromString(result);
		JsonNode toAnalyze = parsed.getNode("result");
		Map<JsonStringNode, JsonNode> fields = toAnalyze.getFields();
		List<ID> converted = new ArrayList<>(5);
		int totalCount = 0;

		for (Entry<JsonStringNode, JsonNode> entry : fields.entrySet()) {
			String name = entry.getKey().getStringValue();
			int number = Integer.parseInt(entry.getValue().getNumberValue());

			if (name.equals("horizontal") ||name.equals("vertical") || name.equals("random")) {
				continue;
			}

			totalCount += number;
			converted.add(new ID(name, number));
		}

		if (converted.size() == 0) {
			System.out.println(".");
		} else if (converted.size() == 1) {
			System.out.println(result);
			if (converted.get(0).count > 4) {
				System.out.println("======> " + converted.get(0).name);
				JOptionPane.showMessageDialog(null, "Detected symbol " + converted.get(0).name);
			} else {
				System.out.println(".");
			}
		} else {
			Collections.sort(converted, new Comparator<ID>() {

				@Override
				public int compare(ID o1, ID o2) {
					return o1.count - o2.count;
				}
			});

			Collections.reverse(converted);
			int max = converted.get(0).count;
			int nextMax = converted.get(1).count;

			System.out.println(result);
			if (((double) max / totalCount > 0.5) && (max - nextMax > 10)) {
				System.out.println("======> " + converted.get(0).name);
				JOptionPane.showMessageDialog(null, "Detected symbol " + converted.get(0).name);
			} else {
				System.out.println("======> random");
			}
		}
	}

	private static class ID {
		private final String name;
		private final int count;

		private ID(String name, int count) {
			this.name = name;
			this.count = count;
		}
	}
}
