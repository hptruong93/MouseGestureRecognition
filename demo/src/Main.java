import java.io.File;
import java.util.LinkedList;
import java.util.List;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import org.jnativehook.keyboard.NativeKeyEvent;
import org.jnativehook.keyboard.NativeKeyListener;
import org.jnativehook.mouse.NativeMouseEvent;
import org.jnativehook.mouse.NativeMouseMotionListener;


public class Main {

	private static boolean log = false;
	private static long time = 0;
	private static long startLog = -1;
	private static List<String> ss = new LinkedList<>();

	public static void main(String[] args) throws NativeHookException, InterruptedException {
		final StringBuffer s = new StringBuffer(1000);

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
					time = 0;
					System.out.println("Released");
					log = false;
					startLog = -1;
					ss.add(s.toString());
					s.delete(0, s.length());
				}
			}

			@Override
			public void nativeKeyPressed(NativeKeyEvent arg0) {
				if (arg0.getKeyCode() == NativeKeyEvent.VC_CONTROL_L) {
					long newTime = System.currentTimeMillis();
					if (newTime - time > 1000) {
						log = true;
						startLog = newTime;
					}
					time = newTime;
				}

			}
		});

		GlobalScreen.addNativeMouseMotionListener(new NativeMouseMotionListener() {

			@Override
			public void nativeMouseMoved(NativeMouseEvent arg0) {
				if (!log) {
					return;
				}
				String x = arg0.getX() + ", " + arg0.getY();

				if (startLog > 0 && System.currentTimeMillis() - startLog < 1000) {
					s.append(x);
					s.append('\n');
				} else {
					System.out.println("CUTCUTCUTCUTCUTCUT");
				}
			}

			@Override
			public void nativeMouseDragged(NativeMouseEvent arg0) {
				// TODO Auto-generated method stub

			}
		});

		Thread.sleep(20000);
		System.out.println("Time...");
		Thread.sleep(2000);
		System.out.println(ss.size());
		GlobalScreen.unregisterNativeHook();


		final String testName = "greater_than";
		long base = System.currentTimeMillis();
		for (String x : ss) {
			base++;
			FileUtility.writeToFile(x.trim(), new File("D:\\test\\" + testName + "\\" + base + ".txt"), false);
		}
	}
}
