import socket
import struct
import os
import time
# TFTP 프로토콜 상수
TFTP_READ = 1
TFTP_WRITE = 2
TFTP_DATA = 3
TFTP_ACK = 4
TFTP_ERROR = 5
BLOCK_SIZE = 512
DEFAULT_TIMEOUT = 5
class TFTPClient:
	def __init__(self, server_ip, port=69):
		self.server_ip = server_ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 		self.sock.settimeout(DEFAULT_TIMEOUT)
	def send_request(self, mode, filename):
		"""RRQ(읽기 요청) 또는 WRQ(쓰기 요청) 전송"""
		request_format = f"!H{len(filename)+1}s{len('octet')+1}s"
		request = struct.pack(request_format, mode, filename.encode(), 		b"octet")
		self.sock.sendto(request, (self.server_ip, self.port))
	def receive_file(self, filename):
		"""서버에서 파일 다운로드"""
		print(f"서버에서 {filename} 다운로드 시작")
		with open(filename, "wb") as file:
			block_number = 1
			while True:
				try:
					# 데이터 패킷 수신
					data, addr = self.sock.recvfrom(BLOCK_SIZE + 						4)
					opcode, block = struct.unpack("!HH", 						data[:4])
					if opcode == TFTP_DATA:
						if block != block_number:
							print(f"블록 번호 불일치: 							{block} (기대값: 							{block_number})")
							Continue
						# 데이터 저장
						file.write(data[4:])
						# ACK 전송
						ack = struct.pack("!HH", 							TFTP_ACK, block)
						self.sock.sendto(ack, addr)
						# 마지막 데이터 블록 확인
						if len(data[4:]) < BLOCK_SIZE:
							print("파일 다운로드 완료.")
							break
							block_number += 1
					except socket.timeout:
						print("타임아웃: 서버 응답 없음")
						Break
def send_file(self, filename):
		"""서버로 파일 업로드"""
		print(f"서버로 {filename} 업로드 시작")
		try:
			with open(filename, "rb") as file:
				block_number = 0
				while True:
					# 데이터 읽기
					data = file.read(BLOCK_SIZE)
					block_number += 1
					# DATA 패킷 전송
					data_packet = struct.pack("!HH", TFTP_DATA, block_number) + data
					self.sock.sendto(data_packet, (self.server_ip, self.port))
					# ACK 수신
					try:
						ack, addr = self.sock.recvfrom(4)
						opcode, ack_block = struct.unpack("!HH", ack)
						if opcode != TFTP_ACK or ack_block != block_number:
							print(f"ACK 오류: 블록 번호 {ack_block} (기대값: {block_number})")
							break
						# 마지막 데이터 블록 확인
						if len(data) < BLOCK_SIZE:
							print("파일 업로드 완료.")
							break
					except socket.timeout:
						print(f"타임아웃: 블록 {block_number}에 대한 서버 응답 없음")
							break
			except FileNotFoundError:
				print(f"파일 {filename}을(를) 찾을 수 없습니다.")
		def close(self):
			self.sock.close()
def main():
	print("TFTP 클라이언트 시작")
	server_ip = input("서버 IP 주소를 입력하세요: ").strip()
	port = input("서버 포트를 입력하세요 (기본값: 69): ").strip()
	port = int(port) if port else 69
	client = TFTPClient(server_ip, port)
	try:
		action = input("다운로드(get) 또는 업로드(put)를 선택하세요 (get/put): ").strip().lower()
		filename = input("파일명을 입력하세요: ").strip()
		if action == "get":
			client.send_request(TFTP_READ, filename)
			client.receive_file(filename)
		elif action == "put":
			client.send_request(TFTP_WRITE, filename)
			client.send_file(filename)
		else:
			print("잘못된 선택입니다. 'get' 또는 'put'을 입력하세요.")
	finally:
		client.close()
		print("클라이언트를 종료합니다.")
if __name__ == "__main__":
	main()