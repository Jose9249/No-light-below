// Importamos clases necesarias para gráficos, eventos y estructura de datos
import java.awt.Color;                   // Para colores en gráficos
import java.awt.Dimension;               // Para manejar dimensiones (ancho, alto)
import java.awt.Graphics;                // Para dibujar en pantalla
import java.awt.Graphics2D;              // Versión más avanzada de Graphics
import java.awt.Point;                   // Representa un punto con coordenadas (x,y)
import java.awt.Rectangle;               // Representa un rectángulo (x,y,ancho,alto)
import java.awt.event.KeyEvent;          // Evento de teclado
import java.awt.event.KeyListener;       // Para escuchar eventos de teclado
import java.awt.image.BufferedImage;     // Imagen en memoria donde dibujar
import java.util.ArrayList;               // Lista dinámica (array que crece)
import java.util.HashSet;                 // Conjunto que no permite duplicados
import java.util.List;                    // Interfaz para listas
import java.util.Set;                     // Interfaz para conjuntos
import javax.swing.JFrame;                // Ventana principal
import javax.swing.JPanel;                // Panel para dibujar
import javax.swing.SwingUtilities;        // Para tareas en el hilo de Swing (GUI)

// Comentarios de cabecera con referencias y autoría
/**
 * Java Procedural 2D Dungeon Generation Test.
 * 
 * References:
 * https://en.wikipedia.org/wiki/Prim%27s_algorithm
 * 
 * Procedural Generation in Godot: Dungeon Generation (part 2) - 
 * https://www.youtube.com/watch?v=U9B39sDIupc
 * 
 * @author Leonardo Ono (ono.leo@gmail.com);
 */

// Clase principal que hereda JPanel para dibujar y escucha teclado
public class View2 extends JPanel implements KeyListener {

    // Imagen en memoria donde se dibuja la mazmorra (120x90 píxeles, RGB)
    private final BufferedImage image 
        = new BufferedImage(120, 90, BufferedImage.TYPE_INT_RGB);
    
    // Número total de puntos aleatorios que se intentan colocar
    private static final int NUMBER_OF_POINTS = 10000;
    
    // Lista para guardar los puntos (centros de habitaciones)
    private final List<Point> points = new ArrayList<>();
    
    // Lista para guardar el árbol (conexiones mínimas entre puntos)
    private final List<Point> tree = new ArrayList<>();
    
    // Tamaño máximo y mínimo de las habitaciones (cuadrados/rectángulos)
    private static final int ROOM_MAX_SIZE = 20;
    private static final int ROOM_MIN_SIZE = 10;
    
    // Distancia mínima permitida entre dos habitaciones
    private static final int ROOM_MIN_DISTANCE = 2;
    
    // Lista para guardar las habitaciones como rectángulos
    private final List<Rectangle> rooms = new ArrayList<>();
    
    // Constructor vacío (no hace nada extra al crear)
    public View2() {
    }
    
    // Método para iniciar el listener de teclado (se llama al empezar)
    public void start() {
        addKeyListener(this);
    }

    // Método para dibujar el JPanel (se llama automáticamente)
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g); // Limpia y prepara el fondo
        draw((Graphics2D) image.getGraphics()); // Dibuja la mazmorra en la imagen
        Graphics2D g2d = (Graphics2D) g; 
        // Dibuja la imagen (mini mapa) escalada a todo el panel
        g2d.drawImage(image, 0, 0, getWidth(), getHeight(), null);
    }
    
    // Método privado para hacer todo el dibujo (habitaciones y caminos)
    private void draw(Graphics2D g) {
        // Limpia la imagen con fondo negro
        g.clearRect(0, 0, image.getWidth(), image.getHeight());

        // Conjuntos para guardar las posiciones X y Y que ya están ocupadas
        Set<Integer> xs = new HashSet<>();
        Set<Integer> ys = new HashSet<>();
        
        // Limpiamos listas antes de generar de nuevo
        points.clear();
        tree.clear();
        rooms.clear();
        
        // Color blanco para dibujar habitaciones inicialmente
        g.setColor(Color.WHITE);

        // Etiqueta para saltar al siguiente ciclo si colisiona la habitación
        outer:
        for (int i = 0; i < NUMBER_OF_POINTS; i++) {
            // Generamos posición aleatoria x e y dentro del margen (10 px)
            int x = (int) (10 + (image.getWidth() - 20) * Math.random());
            int y = (int) (10 + (image.getHeight() - 20) * Math.random());
            Point p = new Point(x, y); // Creamos punto
            
            // Tamaño ancho aleatorio entre el mínimo y máximo definido
            int w = (int) (ROOM_MIN_SIZE 
                    + ((ROOM_MAX_SIZE - ROOM_MIN_SIZE) * Math.random()));
            
            // Tamaño alto aleatorio
            int h = (int) (ROOM_MIN_SIZE 
                    + ((ROOM_MAX_SIZE - ROOM_MIN_SIZE) * Math.random()));
            
            // Creamos un rectángulo para la habitación centrado en p
            Rectangle ra = new Rectangle(p.x - w / 2, p.y - h / 2, w, h);
            
            // Revisamos si la habitación se cruza con alguna ya creada
            for (Rectangle rb : rooms) {
                if (ra.intersects(rb)) {
                    // Si choca, saltamos a la siguiente iteración externa (nuevo punto)
                    continue outer;
                }
            }
            
            // Ajustamos la posición y tamaño para dejar distancia mínima
            ra.x += ROOM_MIN_DISTANCE;
            ra.y += ROOM_MIN_DISTANCE;
            ra.width -= 2 * ROOM_MIN_DISTANCE;
            ra.height -= 2 * ROOM_MIN_DISTANCE;

            // Comprobamos que no choquen con posiciones X o Y prohibidas
            if (xs.contains(ra.x) || xs.contains(ra.x + ra.width / 2) 
                || xs.contains(ra.x + ra.width)
                || ys.contains(ra.y) || ys.contains(ra.y + ra.height / 2) 
                || ys.contains(ra.y + ra.height)) {
                // Si hay colisión, saltamos esta habitación
                continue;
            }

            // Guardamos las posiciones que ahora están ocupadas para futuros checks
            int d = 0;
            xs.add(ra.x + d);
            xs.add(ra.x + ra.width / 2 + d);
            xs.add(ra.x + ra.width + d);
            ys.add(ra.y + d);
            ys.add(ra.y + ra.height / 2 + d);
            ys.add(ra.y + ra.height + d);
            
            // Añadimos la habitación a la lista definitiva
            rooms.add(ra);
            
            // Dibujamos la habitación en azul para que se vea
            g.setColor(Color.BLUE);
            g.draw(ra);
            
            // Guardamos el centro para crear conexiones después
            points.add(p);
        }
        
        // Tomamos el primer punto y lo añadimos al árbol (origen)
        tree.add(points.remove(0));
        
        // Mientras queden puntos sin conectar
        while (!points.isEmpty()) {
            Point a = null;
            Point b = null;
            double minDistance = Double.MAX_VALUE; // Distancia máxima inicial
            
            // Buscamos la conexión más corta entre el árbol y los puntos libres
            for (Point p1 : tree) {
                for (Point p2 : points) {
                    // Calculamos distancia euclidiana
                    double dx = p2.x - p1.x;
                    double dy = p2.y - p1.y;
                    double distance = Math.sqrt(dx * dx + dy * dy);
                    // Si la distancia es menor que la mínima actual
                    if (distance < minDistance) {
                        minDistance = distance; // Actualizamos mínima
                        a = p1; // Punto en el árbol
                        b = p2; // Punto fuera del árbol
                    }
                }
            }
            
            // Por seguridad, si algo falla, tiramos excepción
            if (a == null || b == null) {
                throw new RuntimeException("error ?");
            }
            
            // Quitamos b de puntos libres y lo añadimos al árbol
            points.remove(b);
            tree.add(b);

            // Dibujamos camino (pasillo) en rojo en forma de L (horizontal + vertical)
            g.setColor(Color.RED);
            g.drawLine(a.x, a.y, a.x, b.y);
            g.drawLine(a.x, b.y, b.x, b.y);
        }
        
        // Finalmente, rellenamos cada habitación con color oscuro
        g.setPaintMode();
        for (Rectangle room : rooms) {
            g.setColor(Color.DARK_GRAY);
            g.fillRect(room.x + 1, room.y + 1
                    , room.width - ROOM_MIN_DISTANCE / 2
                    , room.height - ROOM_MIN_DISTANCE / 2);
        }
    }
    
    // Método main que arranca el programa y crea la ventana
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            // Creamos instancia del panel View2
            View2 view = new View2();
            // Establecemos tamaño preferido (ventana grande)
            view.setPreferredSize(new Dimension(800, 600));
            
            // Creamos la ventana JFrame
            JFrame frame = new JFrame();
            // Ponemos título a la ventana
            frame.setTitle("Java Procedural 2D Dungeon Generation Test");
            // Añadimos el panel con nuestro dibujo al contenido de la ventana
            frame.getContentPane().add(view);
            // No permitir redimensionar ventana
            frame.setResizable(false);
            // Ajustamos el tamaño de la ventana al tamaño preferido del panel
            frame.pack();
            // Centrar ventana en pantalla
            frame.setLocationRelativeTo(null);
            // Definir acción cerrar ventana para salir del programa
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            // Hacemos visible la ventana
            frame.setVisible(true);
            // Pedimos foco para que el panel reciba eventos de teclado
            view.requestFocus();
            // Iniciamos el listener de teclado
            view.start();
        });
    }

    // Métodos del KeyListener para eventos de teclado (requeridos aunque estén vacíos)
    @Override
    public void keyTyped(KeyEvent e) {
    }

    @Override
    public void keyPressed(KeyEvent e) {
        // Cuando se pulsa tecla, repintamos para regenerar mazmorra
        repaint();
    }

    @Override
    public void keyReleased(KeyEvent e) {
    }
    
}
