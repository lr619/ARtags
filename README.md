# ARtags
HACKPSU SPRING 2023 project
Projects uses Augmented reality and OpenCV's ArUCo tags modules to detect tags and place images over it 
To run the programs:
  In the cmd line type
  To run specific programs we recommend typing the below commands
  
  *Note: all --type must be valid ArUCo Libraries
  py aruco_generator.py --id <int> --type DICT_6X6_50     
  
  *Note: below command image input can be any of the aruco test images or can be any image with the
            provided colorCard.jpg in it
  py aruco_image_detector.py --image \images\arucoTest1.png --type DICT_6X6_50 
  
  py aruco_image_overlay.py --image \images\ColorCardTest.png --source \images\politicalLudy.png
  
  py aruco_video_detector.py --type <any valid OpenCV ArUCo library>
  
  py aruco_video_overlay.py --input <absolute path to any image>
  
  
 
