#! /usr/local/bin/python3

import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import socket
import struct

# OpenFlow message types
OFPT_HELLO = 0
OFPT_FEATURES_REQUEST = 5
OFPT_FEATURES_REPLY = 6
OFPT_PACKET_IN = 10
OFPT_FLOW_MOD = 14

# Controller IP and port
CONTROLLER_IP = '127.0.0.1'
CONTROLLER_PORT = 80  # Change to port 8080

# Switch IP and port
SWITCH_IP = '127.0.0.1'
SWITCH_PORT = 443

# OpenFlow protocol version
OFP_VERSION = 0x04

# Function to create an OpenFlow message
def create_message(msg_type, body=b''):
    # OpenFlow header: version, type, length, xid
    header = struct.pack('!BBHI', OFP_VERSION, msg_type, 8 + len(body), 0)
    return header + body

# Function to send an OpenFlow message to a switch
def send_message(sock, msg):
    try:
        sock.sendall(msg)
    except Exception as e:
        print(f"Error sending message: {e}")

# Function to receive an OpenFlow message from a switch
def receive_message(sock):
    try:
        data = sock.recv(1024)
        return data
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None

# Function to establish connection with switch
def connect_to_switch():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SWITCH_IP, SWITCH_PORT))
        print('Connected to switch:', (SWITCH_IP, SWITCH_PORT))
        return s
    except Exception as e:
        print(f"Error connecting to switch: {e}")
        return None

# Main function
def main():
    # Establish connection with switch
    switch_socket = connect_to_switch()
    if not switch_socket:
        return

    # Send Hello message
    hello_msg = create_message(OFPT_HELLO)
    send_message(switch_socket, hello_msg)

    # Send Features Request message
    features_request_msg = create_message(OFPT_FEATURES_REQUEST)
    send_message(switch_socket, features_request_msg)

    # Receive and print reply from switch
    reply = receive_message(switch_socket)
    if reply:
        print('Received:', reply)
    
    switch_socket.close()

# Perform SDN data analysis
def perform_data_analysis():
    # Count the number of each OpenFlow message type received
    message_counts = {
        'OFPT_HELLO': 0,
        'OFPT_FEATURES_REQUEST': 0,
        'OFPT_FEATURES_REPLY': 0,
        'OFPT_PACKET_IN': 0,
        'OFPT_FLOW_MOD': 0
    }

    # Establish connection with switch
    switch_socket = connect_to_switch()
    if not switch_socket:
        return

    # Send Features Request message to receive messages from the switch
    features_request_msg = create_message(OFPT_FEATURES_REQUEST)
    send_message(switch_socket, features_request_msg)

    # Receive OpenFlow messages from the switch and count message types
    for _ in range(100):  # Receive 100 messages for demonstration purposes
        reply = receive_message(switch_socket)
        if reply:
            msg_type = struct.unpack('!B', reply[1:2])[0]  # Extract message type
            if msg_type in message_counts:
                message_counts[msg_type] += 1

    switch_socket.close()

    # Plot the counts of different message types
    plt.bar(message_counts.keys(), message_counts.values())
    plt.xlabel('OpenFlow Message Type')
    plt.ylabel('Count')
    plt.title('SDN Data Analysis: OpenFlow Message Types')
    plt.show()

# GUI
root = tk.Tk()
root.title("SDN Controller")
root.geometry("300x150")

run_button = tk.Button(root, text="Run Controller", command=main)
run_button.pack(pady=10)

analyze_button = tk.Button(root, text="Perform Data Analysis", command=perform_data_analysis)
analyze_button.pack(pady=10)

root.mainloop()
