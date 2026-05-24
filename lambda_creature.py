"""
Lambda Creature - A 3Blue1Brown Pi Creature-inspired character for Manim.

This module provides LambdaCreature, an expressive animated character based on
the Greek letter lambda (λ) with a single expressive eye, perfect for educational
animations and mathematical visualizations.

Classes:
    LambdaCreature: Base lambda creature with eye and look-around functionality
    ExpressionLambda: Extended creature with eyebrow expressions
"""

import numpy as np
from manim import (
    VGroup, MathTex, Circle, Arc, VectorizedPoint,
    FadeIn, ApplyFunction, Succession, Rotate,
    UP, DOWN, LEFT, RIGHT, WHITE, BLACK, BLUE, PURPLE,
    PI
)


class LambdaCreature(VGroup):
    """
    A lambda-based creature inspired by 3Blue1Brown's pi creature.
    
    Features a lambda symbol body with a single expressive eye that can look
    around, blink, and track points in the scene. Perfect for creating
    character-driven mathematical animations.
    
    Attributes:
        body (MathTex): The lambda symbol body
        eye_sclera (Circle): The white part of the eye
        pupil (Circle): The dark pupil that can move
        body_color (ManimColor): Color of the lambda body
        eye_color (ManimColor): Color of the eye outline
        pupil_color (ManimColor): Color of the pupil
    
    Examples:
        Create a simple lambda creature:
        >>> creature = LambdaCreature(body_color=BLUE_D, height=2.0)
        
        Make it look at a point:
        >>> creature.look_at(np.array([2, 1, 0]))
        
        Create with custom colors:
        >>> creature = LambdaCreature(
        ...     body_color=RED,
        ...     eye_color=WHITE,
        ...     pupil_color=RED,
        ...     height=1.5
        ... )
    """
    
    def __init__(self, 
                 body_color=BLUE, 
                 eye_color=BLACK, 
                 pupil_color=BLACK,
                 height=1.0,
                 **kwargs):
        """
        Initialize a LambdaCreature.
        
        Args:
            body_color: Color of the lambda symbol (default: BLUE)
            eye_color: Color of the eye outline/sclera (default: BLACK)
            pupil_color: Color of the pupil (default: BLACK)
            height: Height of the lambda body (default: 1.0)
            **kwargs: Additional arguments passed to VGroup
        """
        super().__init__(**kwargs)
        self.body_color = body_color
        self.eye_color = eye_color
        self.pupil_color = pupil_color
        
        # Create lambda body using MathTex
        self.body = MathTex(r"\lambda", color=body_color)
        self.body.height = height
        
        # Create eye (sclera - white part)
        eye_radius = height * 0.12
        self.eye_sclera = Circle(
            radius=eye_radius,
            color=eye_color,
            fill_color=WHITE,
            fill_opacity=1
        )
        
        # Position eye inside the lambda body at 75% height, centered on diagonal line
        body_center = self.body.get_center()
        body_height = self.body.get_height()
        body_width = self.body.get_width()
        
        # Position at 75% height from bottom, centered on the diagonal line
        # Nudged to the left to sit on the thick diagonal stroke
        eye_x = body_center[0] + body_width * 0.0625
        eye_y = body_center[1] + body_height * 0.25
        self.eye_sclera.move_to([eye_x, eye_y, 0])
        
        # Create pupil
        pupil_radius = eye_radius * 0.4
        self.pupil = Circle(
            radius=pupil_radius,
            color=pupil_color,
            fill_color=pupil_color,
            fill_opacity=1,
            stroke_width=0
        )
        self.pupil.move_to(self.eye_sclera.get_center())
        
        # Create highlight/reflection for that 3Blue1Brown pi creature look
        # Small white circle in upper-left area of pupil for glossy appearance
        highlight_radius = pupil_radius * 0.35
        self.highlight = Circle(
            radius=highlight_radius,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0
        )
        # Position highlight to sit on edge of pupil (tangent point at upper-left)
        # Overlap slightly to eliminate any gaps
        tangent_distance = (pupil_radius - highlight_radius) * 0.85
        direction_45 = np.array([-np.sqrt(2)/2, np.sqrt(2)/2, 0])
        self.highlight.move_to(
            self.pupil.get_center() + tangent_distance * direction_45
        )
        
        # Store original positions for reset
        self.pupil_original_position = self.pupil.get_center().copy()
        self.highlight_original_position = self.highlight.get_center().copy()
        
        # Add components to group
        self.add(self.body, self.eye_sclera, self.pupil, self.highlight)
    
    def look_at(self, point):
        """
        Make the creature look at a specific point.
        
        The pupil moves toward the given point while remaining constrained
        within the sclera bounds, creating a natural looking gaze.
        
        Args:
            point: Array-like [x, y, z] coordinate to look at
            
        Returns:
            self: For method chaining
            
        Example:
            >>> creature.look_at(np.array([3, 2, 0]))
        """
        # Calculate direction from eye to point
        eye_center = self.eye_sclera.get_center()
        direction = (point - eye_center)
        direction = direction / np.linalg.norm(direction)  # normalize
        
        # Move pupil in the direction, but keep it within the sclera
        pupil_radius = self.pupil.radius
        sclera_radius = self.eye_sclera.radius
        max_offset = sclera_radius - pupil_radius
        
        new_pupil_position = eye_center + direction * max_offset * 0.7
        self.pupil.move_to(new_pupil_position)
        
        # Move highlight to sit on edge of pupil at upper-left
        tangent_distance = (pupil_radius - self.highlight.radius) * 0.85
        direction_45 = np.array([-np.sqrt(2)/2, np.sqrt(2)/2, 0])
        self.highlight.move_to(
            new_pupil_position + tangent_distance * direction_45
        )
        return self
    
    def blink(self, duration=0.2):
        """
        Return an animation of the creature blinking.
        
        Creates a smooth blink animation where the eye scales down and back up.
        
        Args:
            duration: Duration of the blink in seconds (default: 0.2)
            
        Returns:
            Succession: Animation sequence that can be played with self.play()
            
        Example:
            >>> self.play(creature.blink(duration=0.3))
        """
        return Succession(
            # Close eye (scale down vertically)
            self.eye_sclera.animate.scale(1),  # eye closes
            ApplyFunction(
                lambda m: m.scale(0.1),
                self.eye_sclera,
                run_time=duration/2
            ),
            # Open eye (scale back up)
            ApplyFunction(
                lambda m: m.scale(10),
                self.eye_sclera,
                run_time=duration/2
            ),
        )
    
    def reset_eyes(self):
        """
        Reset pupil to center of eye.
        
        Returns the pupil to the center of the sclera, creating a neutral
        expression.
        
        Returns:
            self: For method chaining
        """
        self.pupil.move_to(self.eye_sclera.get_center())
        # Reset highlight to original position
        self.highlight.move_to(self.highlight_original_position)
        return self
    
    def shift_eye(self, direction):
        """
        Shift the eye in a given direction.
        
        Moves the pupil toward a cardinal direction (UP, DOWN, LEFT, RIGHT).
        
        Args:
            direction: Direction vector (e.g., UP, DOWN, LEFT, RIGHT)
            
        Returns:
            self: For method chaining
            
        Example:
            >>> creature.shift_eye(LEFT)
            >>> creature.shift_eye(UP)
        """
        eye_center = self.eye_sclera.get_center()
        pupil_radius = self.pupil.radius
        sclera_radius = self.eye_sclera.radius
        max_offset = sclera_radius - pupil_radius
        
        new_position = eye_center + direction * max_offset * 0.5
        self.pupil.move_to(new_position)
        
        # Move highlight to sit on edge of pupil at upper-left
        tangent_distance = (pupil_radius - self.highlight.radius) * 0.85
        direction_45 = np.array([-np.sqrt(2)/2, np.sqrt(2)/2, 0])
        self.highlight.move_to(
            new_position + tangent_distance * direction_45
        )
        return self


class ExpressionLambda(LambdaCreature):
    """
    Lambda creature with eyebrow expressions for emotional communication.
    
    Extends LambdaCreature with an animated eyebrow that can express emotions
    like happiness, sadness, and anger, making it great for comedic or
    expressive animations.
    
    Attributes:
        eyebrow (Arc): An arc above the eye that represents the eyebrow
        
    Examples:
        Create an expressive lambda:
        >>> creature = ExpressionLambda(body_color=PURPLE, height=2.0)
        
        Make it happy:
        >>> self.play(creature.happy())
        
        Make it sad:
        >>> self.play(creature.sad())
    """
    
    def __init__(self, **kwargs):
        """
        Initialize an ExpressionLambda.
        
        Args:
            **kwargs: Arguments passed to LambdaCreature.__init__
        """
        super().__init__(**kwargs)
        
        # Add eyebrow
        eyebrow_width = self.eye_sclera.radius * 1.5
        eyebrow_height = self.eye_sclera.radius * 0.3
        
        self.eyebrow = Arc(
            radius=eyebrow_width,
            angle=PI,
            color=self.body_color,
            stroke_width=2
        )
        # Position eyebrow above the eye
        eyebrow_y = self.eye_sclera.get_top()[1] + eyebrow_height
        eyebrow_x = self.eye_sclera.get_center()[0]
        self.eyebrow.move_to([eyebrow_x, eyebrow_y, 0])
        
        self.add(self.eyebrow)
    
    def happy(self):
        """
        Make the creature look happy by raising eyebrow.
        
        Returns:
            Animation: An animation that can be played with self.play()
            
        Example:
            >>> self.play(creature.happy())
        """
        return self.eyebrow.animate.shift(UP * 0.2)
    
    def sad(self):
        """
        Make the creature look sad by lowering eyebrow.
        
        Returns:
            Animation: An animation that can be played with self.play()
            
        Example:
            >>> self.play(creature.sad())
        """
        return self.eyebrow.animate.shift(DOWN * 0.2)
    
    def angry(self):
        """
        Make the creature look angry with eyebrow tilt.
        
        Returns:
            Animation: A rotation animation that can be played with self.play()
            
        Example:
            >>> self.play(creature.angry())
        """
        return Rotate(self.eyebrow, angle=PI / 6)
